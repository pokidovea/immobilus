from immobilus.logic import immobilus, _datetime_to_utc_timestamp

import time
from datetime import datetime

import pytz


def test_mktime_without_timezone():
    with immobilus('1970-01-01 00:00:00'):
        timestamp = _datetime_to_utc_timestamp(datetime.now())

        timetuple = datetime.now().timetuple()
        mktime = time.mktime(timetuple)

        assert mktime == timestamp


def test_mktime_gets_timezone_from_timetuple():
    timezone = pytz.timezone('US/Eastern')
    dt = timezone.localize(datetime(1970, 1, 1, 0, 0))

    with immobilus(dt):
        timetuple = datetime.now().timetuple()
        timestamp = _datetime_to_utc_timestamp(datetime.now())

        mktime = time.mktime(timetuple)
        assert mktime == timestamp
