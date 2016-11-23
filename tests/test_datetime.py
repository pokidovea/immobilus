from immobilus import immobilus

from datetime import datetime

import pytest


@pytest.mark.parametrize('time_function', [datetime.utcnow, datetime.now])
def test_decorator(time_function):

    dt = datetime(2016, 1, 1)
    assert time_function() != dt

    @immobilus('2016-01-01')
    def test():
        assert time_function() == dt

    test()

    assert time_function() != dt


@pytest.mark.parametrize('time_function', [datetime.utcnow, datetime.now])
def test_context_manager(time_function):

    dt = datetime(2016, 1, 1)
    assert time_function() != dt

    with immobilus('2016-01-01'):
        assert time_function() == dt

    assert time_function() != dt


@pytest.mark.parametrize('time_function', [datetime.utcnow, datetime.now])
def test_nested_context_manager(time_function):

    dt1 = datetime(2016, 1, 1)
    dt2 = datetime(2014, 10, 12)
    assert time_function() != dt1
    assert time_function() != dt2

    with immobilus('2016-01-01'):
        assert time_function() == dt1

        with immobilus('2014-10-12'):
            assert time_function() == dt2

        assert time_function() == dt1

    assert time_function() != dt1
    assert time_function() != dt2
