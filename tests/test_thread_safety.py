"""
Tests for thread safety and async context isolation (critical bugs).
"""
import asyncio
import threading
from datetime import datetime

import pytest

from immobilus import immobilus


# ---------------------------------------------------------------------------
# 1. Thread safety
# ---------------------------------------------------------------------------

def test_thread_safety_no_race_condition():
    """
    Two threads freeze different times simultaneously.
    Each thread must see only its own frozen time, not the other thread's.
    """
    errors = []
    iterations = 50

    def freeze_and_check(frozen_str, expected):
        for _ in range(iterations):
            with immobilus(frozen_str):
                got = datetime.utcnow()
                if got != expected:
                    errors.append(
                        f"Thread expected {expected}, got {got}"
                    )

    t1 = threading.Thread(
        target=freeze_and_check,
        args=('2020-01-01 00:00:00', datetime(2020, 1, 1, 0, 0, 0)),
    )
    t2 = threading.Thread(
        target=freeze_and_check,
        args=('2023-06-15 12:00:00', datetime(2023, 6, 15, 12, 0, 0)),
    )

    t1.start()
    t2.start()
    t1.join()
    t2.join()

    assert not errors, "\n".join(errors)


def test_thread_does_not_affect_main_thread():
    """
    A background thread's freeze must not bleed into the main thread.
    """
    barrier = threading.Barrier(2)
    errors = []

    def background():
        with immobilus('2099-12-31 23:59:59'):
            barrier.wait()   # both threads are inside their sections
            barrier.wait()   # hold until main thread has checked

    t = threading.Thread(target=background)
    t.start()

    barrier.wait()
    # Main thread has NOT frozen time — it should see real (non-2099) time
    now = datetime.utcnow()
    if now.year == 2099:
        errors.append(f"Main thread saw background thread's frozen time: {now}")
    barrier.wait()
    t.join()

    assert not errors, "\n".join(errors)


# ---------------------------------------------------------------------------
# 2. Async context isolation
# ---------------------------------------------------------------------------

@pytest.mark.asyncio
async def test_async_context_isolation_between_coroutines():
    """
    Two coroutines freeze different times and await concurrently.
    Each coroutine must see only its own frozen time after resuming from await.
    """
    errors = []

    async def coro_a():
        with immobilus('2020-01-01 00:00:00'):
            await asyncio.sleep(0)          # yield control to event loop
            got = datetime.utcnow()
            if got != datetime(2020, 1, 1):
                errors.append(f"coro_a expected 2020-01-01, got {got}")

    async def coro_b():
        with immobilus('2023-06-15 12:00:00'):
            await asyncio.sleep(0)          # yield control to event loop
            got = datetime.utcnow()
            if got != datetime(2023, 6, 15, 12, 0, 0):
                errors.append(f"coro_b expected 2023-06-15 12:00, got {got}")

    await asyncio.gather(coro_a(), coro_b())

    assert not errors, "\n".join(errors)


@pytest.mark.asyncio
async def test_async_decorator_isolation():
    """
    Two decorated coroutines running concurrently must not interfere.
    """
    errors = []

    @immobilus('2020-01-01 00:00:00')
    async def coro_a():
        await asyncio.sleep(0)
        got = datetime.utcnow()
        if got != datetime(2020, 1, 1):
            errors.append(f"coro_a expected 2020-01-01, got {got}")

    @immobilus('2023-06-15 12:00:00')
    async def coro_b():
        await asyncio.sleep(0)
        got = datetime.utcnow()
        if got != datetime(2023, 6, 15, 12, 0, 0):
            errors.append(f"coro_b expected 2023-06-15 12:00, got {got}")

    await asyncio.gather(coro_a(), coro_b())

    assert not errors, "\n".join(errors)


@pytest.mark.asyncio
async def test_async_context_restored_after_exit():
    """
    After a coroutine's immobilus context exits, time must return to
    whatever it was before (None → real time, or outer frozen time).
    """
    outer_dt = datetime(2000, 1, 1)

    with immobilus('2000-01-01 00:00:00'):
        async def inner():
            with immobilus('2099-12-31 23:59:59'):
                await asyncio.sleep(0)
            # After inner context exits, we should be back to outer freeze
            got = datetime.utcnow()
            assert got == outer_dt, f"Expected {outer_dt}, got {got}"

        await inner()
