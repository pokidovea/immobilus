import pytest
from datetime import datetime, timezone, timedelta

from immobilus import immobilus
from tests.utils import utcnow


def test_jump_with_string():
    with immobilus('2025-01-01 00:00:00') as clock:
        clock.jump('2025-06-15 12:30:00')
        assert utcnow() == datetime(2025, 6, 15, 12, 30, 0)


def test_jump_with_datetime():
    with immobilus('2025-01-01 00:00:00') as clock:
        clock.jump(datetime(2025, 3, 20, 8, 0, 0))
        assert utcnow() == datetime(2025, 3, 20, 8, 0, 0)


def test_jump_with_aware_datetime():
    tz = timezone(timedelta(hours=3))
    with immobilus('2025-01-01 00:00:00') as clock:
        clock.jump(datetime(2025, 3, 20, 11, 0, 0, tzinfo=tz))
        assert utcnow() == datetime(2025, 3, 20, 8, 0, 0)


def test_jump_with_aware_string():
    with immobilus('2025-01-01 00:00:00') as clock:
        clock.jump('2025-03-20 11:00:00+03:00')
        assert utcnow() == datetime(2025, 3, 20, 8, 0, 0)


def test_jump_multiple_times():
    with immobilus('2025-01-01 00:00:00') as clock:
        clock.jump('2025-06-01 00:00:00')
        assert utcnow() == datetime(2025, 6, 1, 0, 0, 0)
        clock.jump(datetime(2025, 12, 31, 23, 59, 59))
        assert utcnow() == datetime(2025, 12, 31, 23, 59, 59)


def test_jump_backward():
    with immobilus('2025-06-15 12:00:00') as clock:
        clock.jump('2025-01-01 00:00:00')
        assert utcnow() == datetime(2025, 1, 1, 0, 0, 0)


def test_jump_does_not_affect_outside_context():
    with immobilus('2025-01-01 00:00:00') as clock:
        clock.jump('2030-01-01 00:00:00')
        assert utcnow() == datetime(2030, 1, 1, 0, 0, 0)
    assert utcnow() != datetime(2030, 1, 1, 0, 0, 0)


def test_jump_invalid_type():
    with immobilus('2025-01-01 00:00:00') as clock:
        with pytest.raises(TypeError):
            clock.jump(12345)
