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


def test_datetime_now_with_timezone_on_py3():
    dt = datetime.now(tz=pytz.utc)

    with immobilus('2016-01-01 13:54'):
        dt1 = datetime.now(tz=pytz.utc)

    assert dt.tzinfo == pytz.utc
    assert dt1.tzinfo == pytz.utc


@pytest.mark.parametrize('datetime_function', [datetime.utcnow, datetime.now])
def test_datetime_now_is_naive(datetime_function):
    assert datetime_function().tzinfo == None
    with immobilus('2017-10-12'):
        assert datetime_function().tzinfo == None
    with immobilus(datetime(2017, 10, 12, tzinfo=pytz.utc)):
        assert datetime_function().tzinfo == None


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
    expected_dt = datetime(1970, 1, 1, 0, 0, tzinfo=None)
    with immobilus('1970-01-01 00:00:01', tz_offset=6):
        dt = datetime.fromtimestamp(0)

        assert dt == expected_dt


def test_fromtimestamp_with_tz():
    timezone = pytz.timezone('US/Eastern')
    expected_dt = datetime(1970, 1, 1, 0, 0, tzinfo=timezone)

    with immobilus('1970-01-01 00:00:01'):
        dt = datetime.fromtimestamp(0, timezone)

        assert dt == expected_dt


def test_fromtimestamp_takes_tz_from_frozen_datetime():
    timezone = pytz.timezone('US/Eastern')
    expected_dt = datetime(1970, 1, 1, 0, 0, tzinfo=timezone)

    with immobilus(datetime(2017, 1, 1, 0, 0, tzinfo=timezone)):
        dt = datetime.fromtimestamp(0)

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
