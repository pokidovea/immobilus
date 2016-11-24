import sys
import time
from datetime import datetime
from functools import wraps

from dateutil import parser

TIME_TO_FREEZE = None


original_time = time.time


def datetime_to_timestamp(dt):
    return time.mktime(dt.timetuple())


def fake_time():
    if TIME_TO_FREEZE is not None:
        return datetime_to_timestamp(TIME_TO_FREEZE)
    else:
        return original_time()


class DatetimeMeta(type):

    @classmethod
    def __instancecheck__(self, obj):
        return isinstance(obj, datetime)


class FakeDatetime(datetime):

    __metaclass__ = DatetimeMeta

    def __add__(self, other):
        result = datetime.__add__(self, other)

        if result is NotImplemented:
            return result

        return self.from_datetime(result)

    def __sub__(self, other):
        result = datetime.__sub__(self, other)

        if result is NotImplemented:
            return result

        if isinstance(result, datetime):
            return self.from_datetime(result)
        else:
            return result

    @classmethod
    def utcnow(cls):
        global TIME_TO_FREEZE

        dt = TIME_TO_FREEZE or datetime.utcnow()
        return cls.from_datetime(dt)

    @classmethod
    def now(cls):
        global TIME_TO_FREEZE

        dt = TIME_TO_FREEZE or datetime.now()
        return cls.from_datetime(dt)

    @classmethod
    def from_datetime(cls, dt):
        return cls(
            dt.year,
            dt.month,
            dt.day,
            dt.hour,
            dt.minute,
            dt.second,
            dt.microsecond,
            dt.tzinfo,
        )


setattr(sys.modules['datetime'], 'datetime', FakeDatetime)
setattr(sys.modules['time'], 'time', fake_time)


class immobilus(object):

    def __init__(self, time_to_freeze):
        self.time_to_freeze = time_to_freeze

    def __call__(self, func):
        return self._decorate_func(func)

    def _decorate_func(self, fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            with self:
                return fn(*args, **kwargs)

        return wrapper

    def __enter__(self):
        global TIME_TO_FREEZE

        self.previous_value = TIME_TO_FREEZE
        TIME_TO_FREEZE = parser.parse(self.time_to_freeze)

        return self.time_to_freeze

    def __exit__(self, *args):
        global TIME_TO_FREEZE
        TIME_TO_FREEZE = self.previous_value
