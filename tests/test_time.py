from immobilus import immobilus
from immobilus.logic import _datetime_to_utc_timestamp

from datetime import datetime
from time import time

import pytz


def test_time_function():

    dt = datetime(1970, 1, 1)
    timestamp = _datetime_to_utc_timestamp(dt)
    assert timestamp == 0.0
    assert type(timestamp) is float
    assert time() != timestamp

    with immobilus(dt):
        assert time() == timestamp

    assert time() != timestamp

    with immobilus(dt.replace(tzinfo=pytz.utc)):
        assert time() == timestamp

    assert time() != timestamp
