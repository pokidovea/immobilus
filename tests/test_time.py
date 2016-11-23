from immobilus import immobilus
from immobilus.logic import datetime_to_timestamp

from datetime import datetime
from time import time


def test_time_function():

    dt = datetime(2016, 1, 1)
    assert time() != datetime_to_timestamp(dt)

    with immobilus('2016-01-01'):
        assert time() == datetime_to_timestamp(dt)

    assert time() != datetime_to_timestamp(dt)
