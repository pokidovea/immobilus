from immobilus import immobilus

from datetime import date, timedelta


def test_decorator():

    dt = date(2016, 1, 1)
    assert date.today() != dt

    @immobilus('2016-01-01')
    def test():
        assert date.today() == dt

    test()

    assert date.today() != dt


def test_context_manager():

    dt = date(2016, 1, 1)
    assert date.today() != dt

    with immobilus('2016-01-01'):
        assert date.today() == dt

    assert date.today() != dt


def test_nested_context_manager():

    dt1 = date(2016, 1, 1)
    dt2 = date(2014, 10, 12)
    assert date.today() != dt1
    assert date.today() != dt2

    with immobilus('2016-01-01'):
        assert date.today() == dt1

        with immobilus('2014-10-12'):
            assert date.today() == dt2

        assert date.today() == dt1

    assert date.today() != dt1
    assert date.today() != dt2


def test_addition():
    dt = date(2016, 1, 1)

    assert dt + timedelta(days=1) == date(2016, 1, 2)


def test_subtraction():
    dt = date(2016, 1, 2)

    assert dt - timedelta(days=1) == date(2016, 1, 1)
