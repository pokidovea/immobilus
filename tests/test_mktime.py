from immobilus.logic import immobilus, datetime_to_utc_timestamp

import time
from datetime import datetime

import pytz


def test_mktime_without_timezone():
    with immobilus('1970-01-01 00:00:00'):
        timetuple = datetime.now().timetuple()
        timestamp = datetime_to_utc_timestamp(datetime.now())

        mktime = time.mktime(timetuple)
        assert mktime == timestamp


def test_mktime_gets_timezone_from_timetuple():
    timezone = pytz.timezone('US/Eastern')
    dt = datetime(1970, 1, 1, 0, 0, tzinfo=timezone)

    with immobilus(dt):
        timetuple = datetime.now().timetuple()
        timestamp = datetime_to_utc_timestamp(datetime.now())

        mktime = time.mktime(timetuple)
        assert mktime == timestamp
