import six

from immobilus import immobilus
from immobilus.logic import original_datetime, FakeDatetime

import pytz
import platform
import time
from datetime import datetime, timedelta

import pytest


@pytest.mark.parametrize('datetime_function', [datetime.utcnow, datetime.now])
def test_decorator(datetime_function):

    dt = datetime(2016, 1, 1, 13, 54)
    assert datetime_function() != dt

    @immobilus('2016-01-01 13:54')
    def test():
        assert datetime_function() == dt

    test()

    assert datetime_function() != dt


@pytest.mark.parametrize('datetime_function', [datetime.utcnow, datetime.now])
def test_context_manager(datetime_function):

    dt = datetime(2016, 1, 1, 13, 54)
    assert datetime_function() != dt

    with immobilus('2016-01-01 13:54'):
        assert datetime_function() == dt

    assert datetime_function() != dt


@pytest.mark.parametrize('datetime_function', [datetime.utcnow, datetime.now])
def test_nested_context_manager(datetime_function):

    dt1 = datetime(2016, 1, 1, 13, 54)
    dt2 = datetime(2014, 10, 12, 16, 42)
    assert datetime_function() != dt1
    assert datetime_function() != dt2

    with immobilus('2016-01-01 13:54'):
        assert datetime_function() == dt1

        with immobilus('2014-10-12 16:42'):
            assert datetime_function() == dt2

        assert datetime_function() == dt1

    assert datetime_function() != dt1
    assert datetime_function() != dt2


@pytest.mark.parametrize('datetime_function', [datetime.utcnow, datetime.now])
def test_start_stop(datetime_function):

    dt = datetime(2016, 1, 1, 13, 54)
    assert datetime_function() != dt

    spell = immobilus('2016-01-01 13:54')
    assert datetime_function() != dt

    try:
        spell.start()
        assert datetime_function() == dt
    finally:
        spell.stop()

    assert datetime_function() != dt


def test_datetime_object():
    dt = datetime(1970, 1, 1)
    with immobilus(dt):
        assert datetime.now() == dt


def test_datetime_each_time_must_be_different():
    dt1 = datetime.utcnow()
    # Sadly, Windows gives us only millisecond resolution, which is
    # insufficient. We have to wait a while for time to move on.
    if platform.system() == 'Windows':
        time.sleep(0.001)
    dt2 = datetime.utcnow()

    assert dt1 != dt2


def test_datetime_now_with_timezone():
    dt = datetime.now(tz=pytz.utc)

    with immobilus('2016-01-01 13:54'):
        dt1 = datetime.now(tz=pytz.utc)

    assert dt.tzinfo == pytz.utc
    assert dt1.tzinfo == pytz.utc


@pytest.mark.parametrize('datetime_function', [datetime.utcnow, datetime.now])
def test_datetime_now_is_naive(datetime_function):
    assert datetime_function().tzinfo is None

    with immobilus('2017-10-12'):
        assert datetime_function().tzinfo is None

    with immobilus(datetime(2017, 10, 12, tzinfo=pytz.utc)):
        assert datetime_function().tzinfo is None


def test_addition():
    dt = datetime(2016, 1, 1, 10, 15)

    assert dt + timedelta(days=1, hours=1, minutes=10) == datetime(2016, 1, 2, 11, 25)


def test_subtraction():
    dt = datetime(2016, 1, 2, 11, 25)

    assert dt - timedelta(days=1, hours=1, minutes=10) == datetime(2016, 1, 1, 10, 15)


def test_tz_offset():
    with immobilus('2016-01-01 13:54', tz_offset=3):
        dt = datetime.now()
        assert dt == datetime.utcnow() + timedelta(hours=3)


def test_tz_offset_timezone_on_py3():
    with immobilus('2016-01-01 13:54', tz_offset=3):
        dt = datetime.now(tz=pytz.utc)

        assert dt.year == (datetime.utcnow() + timedelta(hours=3)).year
        assert dt.month == (datetime.utcnow() + timedelta(hours=3)).month
        assert dt.day == (datetime.utcnow() + timedelta(hours=3)).day

        assert dt.hour == (datetime.utcnow() + timedelta(hours=3)).hour
        assert dt.minute == (datetime.utcnow() + timedelta(hours=3)).minute
        assert dt.second == (datetime.utcnow() + timedelta(hours=3)).second
        assert dt.tzinfo == pytz.utc


def test_fromtimestamp():
    expected_dt = datetime(1970, 1, 1, 0, 0, tzinfo=None)
    with immobilus('1970-01-01 00:00:01'):
        dt = datetime.fromtimestamp(0)

        assert dt == expected_dt


def test_fromtimestamp_with_tz_offset():
    expected_dt = datetime(1970, 1, 1, 6, tzinfo=None)
    with immobilus('1970-01-01 00:00:01', tz_offset=6):
        dt = datetime.fromtimestamp(0)

        assert dt == expected_dt


def test_fromtimestamp_with_tz():
    timezone = pytz.utc
    expected_dt = datetime(1970, 1, 1, 0, 0, tzinfo=timezone)

    with immobilus('1970-01-01 00:00:01'):
        dt = datetime.fromtimestamp(0, timezone)

        assert dt == expected_dt


def test_fromtimestamp_with_tz_when_inactive():
    timezone = pytz.utc
    expected_dt = datetime(1970, 1, 1, 0, 0, tzinfo=timezone)

    dt = datetime.fromtimestamp(0, timezone)
    assert dt == expected_dt


def test_isinstance():
    with immobilus('1970-01-01 00:00:00'):
        mocked_dt = datetime.utcnow()
        assert type(mocked_dt) == FakeDatetime

        original_dt = original_datetime.utcnow()
        assert type(original_dt) != FakeDatetime

        assert isinstance(original_dt, FakeDatetime)
        assert isinstance(mocked_dt, original_datetime)


def test_timestamp_from_naive_datetime_without_offset():
    with immobilus('2017-01-01 00:00:00'):
        dt = datetime(1970, 1, 1, 0, 0)
        if six.PY2:
            with pytest.raises(AttributeError):
                dt.timestamp()
        else:
            assert dt.timestamp() == 0


def test_timestamp_from_naive_datetime_with_offset():
    # Naive datetime instances are assumed to represent local time
    with immobilus('2017-01-01 00:00:00', tz_offset=2):
        dt = datetime(1970, 1, 1, 0, 0)
        if six.PY2:
            with pytest.raises(AttributeError):
                dt.timestamp()
        else:
            assert dt.timestamp() == -2 * 3600


def test_timestamp_from_aware_datetime():
    timezone = pytz.timezone('Europe/Moscow')
    dt = timezone.localize(datetime(1970, 1, 1, 0, 0))

    if six.PY2:
        with pytest.raises(AttributeError):
            dt.timestamp()
    else:
        assert dt.timestamp() == -3 * 3600

    with immobilus('2017-01-01 00:00:00'):
        if six.PY2:
            with pytest.raises(AttributeError):
                dt.timestamp()
        else:
            assert dt.timestamp() == -3 * 3600
