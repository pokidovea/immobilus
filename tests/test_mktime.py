from immobilus.logic import immobilus, _datetime_to_utc_timestamp

import time
from datetime import datetime


def test_without_offset():
    with immobilus('1970-01-01 00:00:00'):
        timestamp = _datetime_to_utc_timestamp(datetime.utcnow())

        timetuple = datetime.utcnow().timetuple()
        mktime = time.mktime(timetuple)

        assert mktime == timestamp


def test_with_positive_offset():
    # UTC (gmt+0) 03:00, Moscow (gmt+3) 06:00
    with immobilus('1970-01-01 03:00:00', tz_offset=3):
        timestamp = _datetime_to_utc_timestamp(datetime.utcnow())  # utc time, 03:00

        timetuple = datetime.now().timetuple()  # local time, 06:00
        mktime = time.mktime(timetuple)

        assert mktime == timestamp == 3 * 3600


def test_with_negative_offset():
    # UTC (gmt+0) 06:00, EST (gmt-5) 01:00
    with immobilus('1970-01-01 06:00:00', tz_offset=-5):
        timestamp = _datetime_to_utc_timestamp(datetime.utcnow())  # utc time, 06:00

        timetuple = datetime.now().timetuple()  # local time, 01:00
        mktime = time.mktime(timetuple)

        assert mktime == timestamp == 6 * 3600
