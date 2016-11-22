from immobilus import immobilus

from datetime import datetime


def test_decorator():

    dt = datetime(2016, 1, 1)
    assert datetime.utcnow() != dt

    @immobilus('2016-01-01')
    def test():
        assert datetime.utcnow() == dt

    test()

    assert datetime.utcnow() != dt


def test_context_manager():

    dt = datetime(2016, 1, 1)
    assert datetime.utcnow() != dt

    with immobilus('2016-01-01'):
        assert datetime.utcnow() == dt

    assert datetime.utcnow() != dt


def test_nested_context_manager():

    dt1 = datetime(2016, 1, 1)
    dt2 = datetime(2014, 10, 12)
    assert datetime.utcnow() != dt1
    assert datetime.utcnow() != dt2

    with immobilus('2016-01-01'):
        assert datetime.utcnow() == dt1

        with immobilus('2014-10-12'):
            assert datetime.utcnow() == dt2

        assert datetime.utcnow() == dt1

    assert datetime.utcnow() != dt1
    assert datetime.utcnow() != dt2
