from immobilus import immobilus

import pytz
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


def test_datetime_each_time_must_be_different():
    dt1 = datetime.utcnow()
    dt2 = datetime.utcnow()

    assert dt1 != dt2


def test_datetime_now_with_timezone_on_py3():
    dt = datetime.now(tz=pytz.utc)

    with immobilus('2016-01-01 13:54'):
        dt1 = datetime.now(tz=pytz.utc)

    assert dt.tzinfo == pytz.utc
    assert dt1.tzinfo == pytz.utc


def test_addition():
    dt = datetime(2016, 1, 1, 10, 15)

    assert dt + timedelta(days=1, hours=1, minutes=10) == datetime(2016, 1, 2, 11, 25)


def test_subtraction():
    dt = datetime(2016, 1, 2, 11, 25)

    assert dt - timedelta(days=1, hours=1, minutes=10) == datetime(2016, 1, 1, 10, 15)
