from immobilus import immobilus
from immobilus.logic import _datetime_to_utc_timestamp

import time
from datetime import datetime


def test_ignore_immobilus_when_seconds_are_set():
    dt = datetime(2016, 1, 1, 14, 56)
    timestamp = _datetime_to_utc_timestamp(dt)

    with immobilus('2015-11-16'):
        time_struct = time.localtime(timestamp)
        assert time_struct.tm_year == 2016
        assert time_struct.tm_mon == 1
        assert time_struct.tm_mday == 1


def test_without_offset():
    with immobilus('2015-11-16 21:35:16'):
        time_struct = time.localtime()
        assert time_struct.tm_year == 2015
        assert time_struct.tm_mon == 11
        assert time_struct.tm_mday == 16
        assert time_struct.tm_hour == 21
        assert time_struct.tm_min == 35
        assert time_struct.tm_sec == 16
        assert time_struct.tm_wday == 0
        assert time_struct.tm_yday == 320
        assert time_struct.tm_isdst == -1

    assert time.localtime().tm_year != 2015


def test_with_positive_offset():
    with immobilus('2015-11-16 21:35:16', tz_offset=3):
        time_struct = time.localtime()
        assert time_struct.tm_year == 2015
        assert time_struct.tm_mon == 11
        assert time_struct.tm_mday == 17
        assert time_struct.tm_hour == 0
        assert time_struct.tm_min == 35
        assert time_struct.tm_sec == 16
        assert time_struct.tm_wday == 1
        assert time_struct.tm_yday == 321
        assert time_struct.tm_isdst == -1

    assert time.localtime().tm_year != 2015


def test_with_negative_offset():
    with immobilus('2015-11-16 21:35:16', tz_offset=-3):
        time_struct = time.localtime()
        assert time_struct.tm_year == 2015
        assert time_struct.tm_mon == 11
        assert time_struct.tm_mday == 16
        assert time_struct.tm_hour == 18
        assert time_struct.tm_min == 35
        assert time_struct.tm_sec == 16
        assert time_struct.tm_wday == 0
        assert time_struct.tm_yday == 320
        assert time_struct.tm_isdst == -1

    assert time.localtime().tm_year != 2015
