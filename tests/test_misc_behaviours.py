"""Tests for moderate issues fixes."""
import pytest
from datetime import datetime
from immobilus import immobilus
from tests.utils import utcnow


def test_call_raises_type_error_for_unsupported_type():
    """__call__ must raise TypeError for unsupported object types."""
    freezer = immobilus("2020-01-01")
    with pytest.raises(TypeError, match="Unsupported object type"):
        freezer(42)


def test_call_works_with_lambda():
    """Lambda is a function — should work, not raise."""
    freezer = immobilus("2020-01-01")
    decorated = freezer(lambda: utcnow())
    assert decorated() == datetime(2020, 1, 1)


def test_call_works_with_regular_function():
    """inspect.isfunction should correctly detect regular functions."""
    freezer = immobilus("2021-06-15 12:00:00")
    def get_now():
        return utcnow()
    decorated = freezer(get_now)
    assert decorated() == datetime(2021, 6, 15, 12, 0, 0)


def test_call_works_with_class():
    """inspect.isclass should correctly detect classes."""
    @immobilus("2022-03-10")
    class MyTests:
        def test_something(self):
            return utcnow()
    obj = MyTests()
    assert obj.test_something() == datetime(2022, 3, 10)


def test_stop_is_idempotent():
    """Calling stop() twice must not raise ValueError."""
    freezer = immobilus("2020-05-05")
    freezer.start()
    freezer.stop()
    freezer.stop()
