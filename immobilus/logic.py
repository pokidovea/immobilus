import six
import sys
import time
import calendar
from datetime import datetime, date, timedelta, tzinfo

from dateutil import parser

try:
    import copy_reg as copyreg
except ImportError:
    import copyreg

TIME_TO_FREEZE = None
TZ_OFFSET = 0


class UTC(tzinfo):
    """UTC"""

    def utcoffset(self, dt):
        return timedelta(0)

    def tzname(self, dt):
        return "UTC"

    def dst(self, dt):
        return timedelta(0)


utc = UTC()

original_mktime = time.mktime
original_time = time.time
original_gmtime = time.gmtime
original_localtime = time.localtime
original_strftime = time.strftime
original_date = date
original_datetime = datetime


def _total_seconds(timedelta):
    """Python 2.6 does not support timedelta.total_seconds() or timedelta/timedelta"""
    return float((timedelta.microseconds + (timedelta.seconds + timedelta.days * 24 * 3600) * 10**6)) / 10**6


def _datetime_to_utc_timestamp(dt):
    assert dt.tzinfo is None
    delta = dt - original_datetime(1970, 1, 1)

    return _total_seconds(delta)


def non_bindable(fn):
    _class_name = fn.__name__ + '_class'

    attrs = {
        '__get__': lambda instance, obj, objtype=None: instance,
        '__call__': lambda instance, *args, **kwargs: fn(*args, **kwargs)
    }

    _class = type(_class_name, (object, ), attrs)
    return _class()


@non_bindable
def fake_time():
    if TIME_TO_FREEZE is not None:
        return _datetime_to_utc_timestamp(TIME_TO_FREEZE)
    else:
        return original_time()


@non_bindable
def fake_localtime(seconds=None):
    if seconds is not None:
        return original_localtime(seconds)

    if TIME_TO_FREEZE is not None:
        return (TIME_TO_FREEZE + timedelta(hours=TZ_OFFSET)).timetuple()
    else:
        return original_localtime()


@non_bindable
def fake_gmtime(seconds=None):
    if seconds is not None:
        return original_gmtime(seconds)

    if TIME_TO_FREEZE is not None:
        return TIME_TO_FREEZE.timetuple()
    else:
        return original_gmtime()


@non_bindable
def fake_strftime(format, t=None):
    if t is not None:
        return original_strftime(format, t)

    if TIME_TO_FREEZE is not None:
        return original_strftime(format, TIME_TO_FREEZE.timetuple())
    else:
        return original_strftime(format)


@non_bindable
def fake_mktime(timetuple):
    # converts local timetuple to utc timestamp
    if TIME_TO_FREEZE is not None:
        return calendar.timegm(timetuple) - _total_seconds(timedelta(hours=TZ_OFFSET))
    else:
        return original_mktime(timetuple)


class DateMeta(type):

    def __instancecheck__(self, obj):
        return isinstance(obj, date)


@six.add_metaclass(DateMeta)
class FakeDate(date):

    def __add__(self, other):
        result = date.__add__(self, other)

        if result is NotImplemented:
            return result

        return self.from_datetime(result)

    def __sub__(self, other):
        result = date.__sub__(self, other)

        if result is NotImplemented:
            return result

        if isinstance(result, date):
            return self.from_datetime(result)
        else:
            return result

    @classmethod
    def today(cls):
        _date = TIME_TO_FREEZE + timedelta(hours=TZ_OFFSET) if TIME_TO_FREEZE else date.today()
        return cls.from_datetime(_date)

    @classmethod
    def from_datetime(cls, _date):
        return cls(
            _date.year,
            _date.month,
            _date.day,
        )


class DatetimeMeta(type):

    def __instancecheck__(self, obj):
        return isinstance(obj, datetime)


@six.add_metaclass(DatetimeMeta)
class FakeDatetime(datetime):

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
        if TIME_TO_FREEZE:
            _datetime = TIME_TO_FREEZE
        else:
            _datetime = datetime.utcnow()

        return cls.from_datetime(_datetime)

    @classmethod
    def now(cls, tz=None):
        assert tz is None or isinstance(tz, tzinfo)
        if TIME_TO_FREEZE:
            if tz:
                _datetime = TIME_TO_FREEZE.replace(tzinfo=utc).astimezone(tz)
            else:
                _datetime = TIME_TO_FREEZE + timedelta(hours=TZ_OFFSET)
        else:
            _datetime = datetime.now(tz=tz)

        return cls.from_datetime(_datetime)

    @classmethod
    def fromtimestamp(cls, timestamp, tz=None):
        assert tz is None or isinstance(tz, tzinfo)

        if TIME_TO_FREEZE and tz is None:
            # Standard library docs say
            # the timestamp is converted to the platform's local date and time,
            # and the returned datetime object is naive.
            _datetime = (
                original_datetime.fromtimestamp(timestamp, utc).replace(tzinfo=None) +
                timedelta(hours=TZ_OFFSET)
            )
        else:
            _datetime = original_datetime.fromtimestamp(timestamp, tz)

        return _datetime

    @classmethod
    def from_datetime(cls, _datetime):
        return cls(
            _datetime.year,
            _datetime.month,
            _datetime.day,
            _datetime.hour,
            _datetime.minute,
            _datetime.second,
            _datetime.microsecond,
            _datetime.tzinfo,
        )

    def timestamp(self):
        if not six.PY3:
            raise AttributeError('\'datetime.datetime\' object has no attribute \'timestamp\'')

        if TIME_TO_FREEZE:
            if self.tzinfo:
                return _datetime_to_utc_timestamp(self.astimezone(utc).replace(tzinfo=None))
            else:
                return _datetime_to_utc_timestamp(self - timedelta(hours=TZ_OFFSET))
        else:
            return super(FakeDatetime, self).timestamp()

    @property
    def nanosecond(self):
        try:
            return TIME_TO_FREEZE.nanosecond
        except AttributeError:
            return 0


def pickle_fake_date(datetime_):
    # A pickle function for FakeDate
    return FakeDate, (
        datetime_.year,
        datetime_.month,
        datetime_.day,
    )


def pickle_fake_datetime(datetime_):
    # A pickle function for FakeDatetime
    return FakeDatetime, (
        datetime_.year,
        datetime_.month,
        datetime_.day,
        datetime_.hour,
        datetime_.minute,
        datetime_.second,
        datetime_.microsecond,
        datetime_.tzinfo,
    )


copyreg.dispatch_table[original_datetime] = pickle_fake_datetime
copyreg.dispatch_table[original_date] = pickle_fake_date

setattr(sys.modules['datetime'], 'date', FakeDate)
setattr(sys.modules['datetime'], 'datetime', FakeDatetime)
setattr(sys.modules['time'], 'time', fake_time)
setattr(sys.modules['time'], 'localtime', fake_localtime)
setattr(sys.modules['time'], 'gmtime', fake_gmtime)
setattr(sys.modules['time'], 'strftime', fake_strftime)
setattr(sys.modules['time'], 'mktime', fake_mktime)


class _immobilus(object):

    def __init__(self, time_to_freeze, tz_offset=0):
        self.time_to_freeze = time_to_freeze
        self.tz_offset = tz_offset

    def __call__(self, obj):
        if type(obj).__name__ == 'function':
            return self._decorate_func(obj)
        if type(obj).__name__ == 'type':
            return self._decorate_class(obj)

    def _decorate_func(self, fn):
        @six.wraps(fn)
        def wrapper(*args, **kwargs):
            with self:
                return fn(*args, **kwargs)

        return wrapper

    def _decorate_class(self, cls):
        class _Meta(type):
            def __new__(cls, name, bases, attrs):
                for attr_name, attr in attrs.items():
                    if callable(attr):
                        attrs[attr_name] = self(attr)

                return super(_Meta, cls).__new__(cls, name, bases, attrs)

        return six.add_metaclass(_Meta)(cls)

    def __enter__(self):
        self.start()

    def __exit__(self, *args):
        self.stop()

    def start(self):
        global TIME_TO_FREEZE
        global TZ_OFFSET

        self.previous_time_to_freeze = TIME_TO_FREEZE
        self.previous_tz_offset = TZ_OFFSET

        if isinstance(self.time_to_freeze, original_date):
            TIME_TO_FREEZE = self.time_to_freeze
            # Convert to a naive UTC datetime if necessary
            if TIME_TO_FREEZE.tzinfo:
                TIME_TO_FREEZE = TIME_TO_FREEZE.astimezone(utc).replace(tzinfo=None)
        else:
            TIME_TO_FREEZE = parser.parse(self.time_to_freeze)

        TZ_OFFSET = self.tz_offset

        return self.time_to_freeze

    def stop(self):
        global TIME_TO_FREEZE
        global TZ_OFFSET

        TIME_TO_FREEZE = self.previous_time_to_freeze
        TZ_OFFSET = self.previous_tz_offset


if sys.version_info[0:2] >= (3, 5):
    six.exec_("""
from asyncio import iscoroutinefunction

class immobilus(_immobilus):

    def __call__(self, func):
        if iscoroutinefunction(func):
            return self._decorate_coroutine(func)

        return super().__call__(func)

    def _decorate_coroutine(self, coro):
        @six.wraps(coro)
        async def wrapper(*args, **kwargs):
            with self:
                return await coro(*args, **kwargs)

        return wrapper
""")
else:
    immobilus = _immobilus
