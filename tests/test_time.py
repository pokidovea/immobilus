from immobilus import immobilus
from immobilus.logic import datetime_to_timestamp

from datetime import datetime
from time import time


def test_time_function():

    dt = datetime(1970, 1, 1)
    assert datetime_to_timestamp(dt) == 0
    assert time() != datetime_to_timestamp(dt)

    with immobilus(dt):
        assert time() == datetime_to_timestamp(dt)

    assert time() != datetime_to_timestamp(dt)
