import time
from datetime import datetime, date

import pytest

from tests.utils import utcnow


@pytest.mark.immobilus('2025-01-01 00:00:00')
def test_marker_freezes_datetime_now():
    assert datetime.now() == datetime(2025, 1, 1, 0, 0, 0)


@pytest.mark.immobilus('2025-01-01 00:00:00')
def test_marker_freezes_datetime_utcnow():
    assert utcnow() == datetime(2025, 1, 1, 0, 0, 0)


@pytest.mark.immobilus('2025-01-01 00:00:00')
def test_marker_freezes_date_today():
    assert date.today() == date(2025, 1, 1)


@pytest.mark.immobilus('2025-01-01 00:00:00')
def test_marker_freezes_time_time():
    assert time.time() == datetime(2025, 1, 1, 0, 0, 0).timestamp()


@pytest.mark.immobilus('2025-06-15 12:00:00', tz_offset=3)
def test_marker_tz_offset():
    assert utcnow() == datetime(2025, 6, 15, 12, 0, 0)
    assert datetime.now() == datetime(2025, 6, 15, 15, 0, 0)


@pytest.mark.immobilus('2025-01-01 00:00:00', tick=True)
def test_marker_tick_starts_from_frozen():
    t = datetime.now()
    assert t.year == 2025
    assert t.month == 1
    assert t.day == 1


@pytest.mark.immobilus('2025-01-01 00:00:00', tick=True)
def test_marker_tick_advances():
    t1 = datetime.now()
    time.sleep(0.1)
    t2 = datetime.now()
    assert t2 > t1


def test_no_marker_does_not_freeze():
    assert datetime.now() != datetime(2025, 1, 1, 0, 0, 0)
