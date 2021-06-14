import asyncio

from immobilus import immobilus

from datetime import datetime

import pytest


@pytest.mark.asyncio
@immobilus('2000-02-01 13:23')
async def test_decorated_async_function():
    assert datetime.utcnow() == datetime(2000, 2, 1, 13, 23)


@pytest.mark.asyncio
async def test_decorated_async_function():
    dt = datetime(2016, 1, 1, 13, 54)
    assert datetime.utcnow() != dt

    with immobilus('2016-01-01 13:54'):
        assert datetime.utcnow() == dt

    assert datetime.utcnow() != dt


@immobilus('2017-10-20')
async def some_coroutine():
    return datetime.now()


def test_coroutine():
    loop = asyncio.new_event_loop()
    result = loop.run_until_complete(some_coroutine())
    assert result.strftime('%Y-%m-%d %H:%M:%S') == '2017-10-20 00:00:00'

