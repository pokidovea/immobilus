import sys
from datetime import datetime
from functools import wraps

from dateutil import parser

TIME_TO_FREEZE = None


class Datetime(datetime):

    @classmethod
    def utcnow(cls):
        global TIME_TO_FREEZE

        if TIME_TO_FREEZE is not None:
            return TIME_TO_FREEZE
        else:
            return datetime.utcnow()

    @classmethod
    def now(cls):
        global TIME_TO_FREEZE

        if TIME_TO_FREEZE is not None:
            return TIME_TO_FREEZE
        else:
            return datetime.now()


setattr(sys.modules['datetime'], 'datetime', Datetime)


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
