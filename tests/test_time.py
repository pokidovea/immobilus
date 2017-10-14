from immobilus import immobilus
from immobilus.logic import _datetime_to_utc_timestamp

from datetime import datetime
from time import time


def test_time_function():

    dt = datetime(1970, 1, 1)
    assert _datetime_to_utc_timestamp(dt) == 0.0
    assert type(_datetime_to_utc_timestamp(dt)) is float
    assert time() != _datetime_to_utc_timestamp(dt)

    with immobilus(dt):
        assert time() == _datetime_to_utc_timestamp(dt)

    assert time() != _datetime_to_utc_timestamp(dt)
