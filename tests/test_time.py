from immobilus import immobilus

from datetime import datetime
from time import time


def test_time_function():

    dt = datetime(2016, 1, 1)
    assert time() != dt.timestamp()

    with immobilus('2016-01-01'):
        assert time() == dt.timestamp()

    assert time() != dt.timestamp()
