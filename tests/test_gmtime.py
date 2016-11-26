from immobilus import immobilus

import time


def test_gmtime():
    with immobilus('2015-11-16 21:35:16'):
        time_struct = time.gmtime()
        assert time_struct.tm_year == 2015
        assert time_struct.tm_mon == 11
        assert time_struct.tm_mday == 16
        assert time_struct.tm_hour == 21
        assert time_struct.tm_min == 35
        assert time_struct.tm_sec == 16
        assert time_struct.tm_wday == 0
        assert time_struct.tm_yday == 320
        assert time_struct.tm_isdst == -1

    assert time.gmtime().tm_year != 2015
