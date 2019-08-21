from immobilus.logic import immobilus

import time
from datetime import datetime, timedelta


def test_transmutations():
    now = datetime.now()
    timetuple = now.timetuple()
    mktime = time.mktime(timetuple)
    fromtimestamp = datetime.fromtimestamp(mktime)

    assert now.replace(microsecond=0) == fromtimestamp

    with immobilus('1970-01-01 00:00:00', tz_offset=2):
        now = datetime.now()
        timetuple = now.timetuple()
        mktime = time.mktime(timetuple)
        fromtimestamp = datetime.fromtimestamp(mktime)

        assert now.replace(microsecond=0) == fromtimestamp


def test_tick():
    with immobilus('2019-08-21 12:00:00') as dt:
        assert datetime(2019, 8, 21, 12, 0, 0) == datetime.now()
        dt.tick()
        assert datetime(2019, 8, 21, 12, 0, 1) == datetime.now()
        dt.tick(timedelta(seconds=10))
        assert datetime(2019, 8, 21, 12, 0, 11) == datetime.now()
