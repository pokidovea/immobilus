import time
from contextlib import contextmanager

import pytest


@pytest.fixture()
def set_timezone():

    @contextmanager
    def factory(new_timezone):
        original_timezone = time.timezone
        time.timezone = new_timezone

        yield

        time.timezone = original_timezone

    return factory
