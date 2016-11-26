from immobilus import immobilus
from immobilus.logic import datetime_to_timestamp

import time
from datetime import datetime


def test_ignore_immobilus_when_seconds_are_set():

    dt = datetime(2016, 1, 1, 14, 56)
    timestamp = datetime_to_timestamp(dt)

    with immobilus('2015-11-16'):
        time_struct = time.localtime(timestamp)
        assert time_struct.tm_year == 2016
        assert time_struct.tm_mon == 1
        assert time_struct.tm_mday == 1
        assert time_struct.tm_hour == 14
        assert time_struct.tm_min == 56
        assert time_struct.tm_sec == 0
        assert time_struct.tm_wday == 4
        assert time_struct.tm_yday == 1
        assert time_struct.tm_isdst == 0


def test_seconds_are_not_set(set_timezone):
    with set_timezone(-10800):
        with immobilus('2015-11-16 21:35:16'):
            time_struct = time.localtime()
            assert time_struct.tm_year == 2015
            assert time_struct.tm_mon == 11
            assert time_struct.tm_mday == 16
            assert time_struct.tm_hour == 18  # offset 3 hours
            assert time_struct.tm_min == 35
            assert time_struct.tm_sec == 16
            assert time_struct.tm_wday == 0
            assert time_struct.tm_yday == 320
            assert time_struct.tm_isdst == -1

        assert time.localtime().tm_year != 2015
