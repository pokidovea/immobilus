from immobilus import immobilus
from immobilus.logic import original_date, FakeDate

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


def test_tz_offset():
    with immobilus('2016-01-01 21:00'):
        dt1 = date.today()

    with immobilus('2016-01-01 21:00', tz_offset=3):
        dt2 = date.today()

    assert dt1 == dt2 - timedelta(days=1)


def test_isinstance():
    with immobilus('1970-01-01 00:00:00'):
        mocked_dt = date.today()
        assert type(mocked_dt) == FakeDate

        original_dt = original_date.today()
        assert type(original_dt) != FakeDate

        assert isinstance(original_dt, FakeDate)
        assert isinstance(mocked_dt, original_date)
