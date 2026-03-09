from immobilus import immobilus
from tests.utils import utcnow
from datetime import datetime


def test_shift_seconds():
    with immobilus('2025-01-01 00:00:00') as clock:
        clock.shift(seconds=30)
        assert utcnow() == datetime(2025, 1, 1, 0, 0, 30)


def test_shift_minutes():
    with immobilus('2025-01-01 00:00:00') as clock:
        clock.shift(minutes=5)
        assert utcnow() == datetime(2025, 1, 1, 0, 5, 0)


def test_shift_hours():
    with immobilus('2025-01-01 00:00:00') as clock:
        clock.shift(hours=3)
        assert utcnow() == datetime(2025, 1, 1, 3, 0, 0)


def test_shift_days():
    with immobilus('2025-01-01 00:00:00') as clock:
        clock.shift(days=10)
        assert utcnow() == datetime(2025, 1, 11, 0, 0, 0)


def test_shift_weeks():
    with immobilus('2025-01-01 00:00:00') as clock:
        clock.shift(weeks=2)
        assert utcnow() == datetime(2025, 1, 15, 0, 0, 0)


def test_shift_combined():
    with immobilus('2025-01-01 00:00:00') as clock:
        clock.shift(weeks=1, days=3, hours=4, minutes=5, seconds=6)
        assert utcnow() == datetime(2025, 1, 11, 4, 5, 6)


def test_shift_negative():
    with immobilus('2025-06-15 12:00:00') as clock:
        clock.shift(days=-5)
        assert utcnow() == datetime(2025, 6, 10, 12, 0, 0)


def test_shift_multiple_times():
    with immobilus('2025-01-01 00:00:00') as clock:
        clock.shift(seconds=10)
        assert utcnow() == datetime(2025, 1, 1, 0, 0, 10)
        clock.shift(seconds=20)
        assert utcnow() == datetime(2025, 1, 1, 0, 0, 30)


def test_shift_does_not_affect_outside_context():
    with immobilus('2025-01-01 00:00:00') as clock:
        clock.shift(days=5)
        assert utcnow() == datetime(2025, 1, 6, 0, 0, 0)
    # Outside context, real time is used
    assert utcnow() != datetime(2025, 1, 6, 0, 0, 0)
