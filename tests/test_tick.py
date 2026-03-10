import time
from datetime import datetime, date

from immobilus import immobilus
from tests.utils import utcnow

FREEZE_TIME = '2025-01-01 00:00:00'
SLEEP_DURATION = 0.1
MIN_ELAPSED = 0.05


# --- tick=False: all methods return frozen time ---

def test_tick_false_datetime_now_frozen():
    with immobilus(FREEZE_TIME, tick=False):
        t1 = datetime.now()
        time.sleep(SLEEP_DURATION)
        t2 = datetime.now()
        assert t1 == t2


def test_tick_false_datetime_utcnow_frozen():
    with immobilus(FREEZE_TIME, tick=False):
        t1 = utcnow()
        time.sleep(SLEEP_DURATION)
        t2 = utcnow()
        assert t1 == t2


def test_tick_false_date_today_frozen():
    with immobilus(FREEZE_TIME, tick=False):
        d1 = date.today()
        time.sleep(SLEEP_DURATION)
        d2 = date.today()
        assert d1 == d2


def test_tick_false_time_time_frozen():
    with immobilus(FREEZE_TIME, tick=False):
        t1 = time.time()
        time.sleep(SLEEP_DURATION)
        t2 = time.time()
        assert t1 == t2


def test_tick_false_time_gmtime_frozen():
    with immobilus(FREEZE_TIME, tick=False):
        t1 = time.gmtime()
        time.sleep(SLEEP_DURATION)
        t2 = time.gmtime()
        assert t1 == t2


def test_tick_false_time_localtime_frozen():
    with immobilus(FREEZE_TIME, tick=False):
        t1 = time.localtime()
        time.sleep(SLEEP_DURATION)
        t2 = time.localtime()
        assert t1 == t2


def test_tick_false_time_strftime_frozen():
    with immobilus(FREEZE_TIME, tick=False):
        s1 = time.strftime('%Y-%m-%d %H:%M:%S')
        time.sleep(SLEEP_DURATION)
        s2 = time.strftime('%Y-%m-%d %H:%M:%S')
        assert s1 == s2


# --- tick=True: all methods start from frozen time ---

def test_tick_true_datetime_now_starts_from_frozen():
    with immobilus(FREEZE_TIME, tick=True):
        t = datetime.now()
        assert t.year == 2025
        assert t.month == 1
        assert t.day == 1


def test_tick_true_datetime_now_advances():
    with immobilus(FREEZE_TIME, tick=True):
        t1 = datetime.now()
        time.sleep(SLEEP_DURATION)
        t2 = datetime.now()
        assert t2 > t1
        assert (t2 - t1).total_seconds() >= MIN_ELAPSED


def test_tick_true_datetime_utcnow_starts_from_frozen():
    with immobilus(FREEZE_TIME, tick=True):
        t = utcnow()
        assert t.year == 2025
        assert t.month == 1
        assert t.day == 1


def test_tick_true_datetime_utcnow_advances():
    with immobilus(FREEZE_TIME, tick=True):
        t1 = utcnow()
        time.sleep(SLEEP_DURATION)
        t2 = utcnow()
        assert t2 > t1
        assert (t2 - t1).total_seconds() >= MIN_ELAPSED


def test_tick_true_date_today_starts_from_frozen():
    with immobilus(FREEZE_TIME, tick=True):
        d = date.today()
        assert d.year == 2025
        assert d.month == 1
        assert d.day == 1


def test_tick_true_time_time_starts_from_frozen():
    with immobilus(FREEZE_TIME, tick=True):
        ts = time.time()
        frozen_ts = datetime(2025, 1, 1).timestamp()
        assert ts >= frozen_ts


def test_tick_true_time_time_advances():
    with immobilus(FREEZE_TIME, tick=True):
        t1 = time.time()
        time.sleep(SLEEP_DURATION)
        t2 = time.time()
        assert t2 > t1
        assert (t2 - t1) >= MIN_ELAPSED


def test_tick_true_time_gmtime_starts_from_frozen():
    with immobilus(FREEZE_TIME, tick=True):
        t = time.gmtime()
        assert t.tm_year == 2025
        assert t.tm_mon == 1
        assert t.tm_mday == 1


def test_tick_true_time_gmtime_advances():
    with immobilus(FREEZE_TIME, tick=True):
        t1 = time.gmtime()
        time.sleep(1.1)
        t2 = time.gmtime()
        assert t2 > t1


def test_tick_true_time_localtime_starts_from_frozen():
    with immobilus(FREEZE_TIME, tick=True):
        t = time.localtime()
        assert t.tm_year == 2025
        assert t.tm_mon == 1
        assert t.tm_mday == 1


def test_tick_true_time_localtime_advances():
    with immobilus(FREEZE_TIME, tick=True):
        t1 = time.localtime()
        time.sleep(SLEEP_DURATION)
        t2 = time.localtime()
        assert t2 >= t1


def test_tick_true_time_strftime_starts_from_frozen():
    with immobilus(FREEZE_TIME, tick=True):
        s = time.strftime('%Y-%m-%d')
        assert s == '2025-01-01'
