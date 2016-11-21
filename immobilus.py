import sys
import os
from datetime import datetime
from functools import wraps

from dateutil import parser


class DatetimeMeta(type):

    def __new__(cls, name, bases, dct):
        klass = super(DatetimeMeta, cls).__new__(cls, name, bases, dct)
        setattr(sys.modules['datetime'], 'datetime', klass)
        return klass


class Datetime(datetime):

    __metaclass__ = DatetimeMeta

    @classmethod
    def utcnow(cls):
        if 'MYDATE' in os.environ:
            return parser.parse(os.getenv('MYDATE'))
        else:
            return datetime.utcnow()


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
        os.environ['MYDATE'] = self.time_to_freeze

    def __exit__(self, *args):
        os.environ.pop('MYDATE')
