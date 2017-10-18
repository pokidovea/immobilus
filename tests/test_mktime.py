from immobilus.logic import immobilus, _datetime_to_utc_timestamp, _total_seconds

import time
from datetime import datetime, timedelta


def test_without_offset():
    with immobilus('1970-01-01 00:00:00'):
        timestamp = _datetime_to_utc_timestamp(datetime.utcnow())

        timetuple = datetime.utcnow().timetuple()
        mktime = time.mktime(timetuple)

        assert mktime == timestamp


def test_with_positive_offset():
    # UTC (gmt+0) 03:00, Moscow (gmt+3) 06:00
    with immobilus('1970-01-01 03:00:00', tz_offset=3):
        timestamp = _datetime_to_utc_timestamp(datetime.utcnow()) + _total_seconds(timedelta(hours=3))

        timetuple = datetime.utcnow().timetuple()
        mktime = time.mktime(timetuple)

        assert mktime == timestamp == 6 * 3600


def test_with_negative_offset():
    # UTC (gmt+0) 06:00, EST (gmt-5) 01:00
    with immobilus('1970-01-01 06:00:00', tz_offset=-5):
        timestamp = _datetime_to_utc_timestamp(datetime.utcnow()) - _total_seconds(timedelta(hours=5))

        timetuple = datetime.utcnow().timetuple()
        mktime = time.mktime(timetuple)

        assert mktime == timestamp == 3600
