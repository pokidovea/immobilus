# immobilus

[![Download from PyPI](https://img.shields.io/pypi/v/immobilus)](https://pypi.python.org/pypi/immobilus)
![Tests](https://github.com/pokidovea/immobilus/actions/workflows/run_tests.yml/badge.svg)

**immobilus** is a lightweight and fast time management library for Python tests. Unlike solutions that perform mass monkeypatching of modules, immobilus intercepts the time source early at import time, adding virtually no runtime overhead even in large test suites.

The library allows you not only to freeze time, but also to control its flow: start time from a given point (`tick=True`), shift it forward (`shift()`), or instantly jump to a specific moment (`jump()`). This makes it a convenient tool for testing time-dependent logic — TTL, expiration, retry/backoff, schedulers, and other time-sensitive systems.

The primary goal of immobilus is to provide deterministic and fast tests, especially in large projects where traditional libraries can significantly slow down execution due to complex monkeypatching.

It mocks:
* `datetime.date.today()`
* `datetime.datetime.now()`
* `datetime.datetime.utcnow()`
* `datetime.datetime.fromtimestamp()`
* `time.time()`
* `time.gmtime()`
* `time.localtime()`
* `time.strftime()`
* `time.mktime()`

## Usage
You must `import immobilus` *before* `datetime` or `time`, or any other module which imports them in turn, to allow it to intercept those modules.

```python
>>> from immobilus import immobilus
>>> from datetime import datetime, timedelta

```

> ✅ **pytest users:** When `immobilus` is installed, early loading is guaranteed automatically via a built-in pytest plugin registered via the `pytest11` entry point. You don't need to manually add `import immobilus` to `conftest.py` — pytest will load `immobilus` before any test modules are imported.

#### Context manager

You can use `immobilus` as a context manager. When the context manager is active, time is frozen to the specified value. Outside of the context manager, the original standard library functions are used and time behaves normally.

```python
>>> # It is unlikely that you are living in the past
>>> datetime.utcnow() == datetime(2017, 10, 20)
False
>>> # But with immobilus, you can pretend that you are
>>> with immobilus('2017-10-20'):
...     datetime.utcnow() == datetime(2017, 10, 20)
...
True
>>> # Once the context manager exits, immobilus deactivates.
>>> # We are back in the present.
>>> datetime.utcnow() == datetime(2017, 10, 20)
False

```

#### Specifying the freeze time

As shown above, you can use a string to describe the time to be frozen (e.g. `'2017-10-20'`). Any values understood by the [dateutil.parser](https://dateutil.readthedocs.io/en/stable/parser.html) can be used.

You can also use a `datetime.datetime` object for the freeze time:

```python
>>> naive_freeze_time = datetime(2017, 10, 20)
>>> with immobilus(naive_freeze_time):
...     print('now:    %s' % datetime.now())
...     print('utcnow: %s' % datetime.utcnow())
...
now:    2017-10-20 00:00:00
utcnow: 2017-10-20 00:00:00

```

`immobilus` will use the given `datetime` object to set the frozen UTC time *and* local time to the same value that you provide. If the `datetime` you provide for the freeze time is aware, then it is adjusted to UTC like so:

```python
>>> import pytz
>>>
>>> # Freeze to 12:00 noon in Moscow (UTC+3)
>>> timezone = pytz.timezone('Europe/Moscow')
>>> aware_freeze_time = timezone.localize(datetime(2017, 10, 20, 12))
>>> with immobilus(aware_freeze_time):
...     # 9:00am local time which is same as UTC
...     print('now:    %s' % datetime.now())
...     print('utcnow: %s' % datetime.utcnow())
...
now:    2017-10-20 09:00:00
utcnow: 2017-10-20 09:00:00

```

If you want local time to differ from UTC, read on.

#### Freezing a local time that is not UTC time

To have a different timezone in effect when time is frozen, use the second argument to the `immobilus` context manager: `tz_offset`. This is the number of hours ahead of the frozen UTC time that the frozen local time should be.

```python
>>> with immobilus('2017-10-20 09:00', tz_offset=3):
...     print('now:    %s' % datetime.now())
...     print('utcnow: %s' % datetime.utcnow())
...
now:    2017-10-20 12:00:00
utcnow: 2017-10-20 09:00:00

```

Of course, you can be behind UTC if you wish, by using a negative number:

```python
>>> with immobilus('2017-10-20 09:00', tz_offset=-7):
...     print('now:    %s' % datetime.now())
...     print('utcnow: %s' % datetime.utcnow())
...
now:    2017-10-20 02:00:00
utcnow: 2017-10-20 09:00:00

```

#### Letting time tick from a frozen point

By default, time is completely frozen. If you want time to continue flowing from the frozen point, use `tick=True`:

```python
>>> import time
>>> with immobilus('2025-01-01 00:00:00', tick=True):
...     print(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))   # starts at the frozen time
...     time.sleep(2)
...     print(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))   # 2 seconds have passed
...
2025-01-01 00:00:00
2025-01-01 00:00:02

```

This works for all mocked functions: `datetime.now()`, `datetime.utcnow()`, `date.today()`, `time.time()`, `time.gmtime()`, `time.localtime()`, and `time.strftime()`.

Outside the context manager, the original system time is restored:

```python
>>> datetime.utcnow() == datetime(2025, 1, 1)
False

```

#### Shifting frozen time

You can shift the frozen time forward (or backward) by a given amount using the `shift` method on the clock object returned by the context manager. It accepts `weeks`, `days`, `hours`, `minutes`, and `seconds` as keyword arguments:

```python
>>> with immobilus('2025-01-01 00:00:00') as clock:
...     clock.shift(seconds=30)
...     print(datetime.utcnow())
...
2025-01-01 00:00:30

```

You can combine multiple units in a single call:

```python
>>> with immobilus('2025-01-01 00:00:00') as clock:
...     clock.shift(weeks=1, days=3, hours=4, minutes=5, seconds=6)
...     print(datetime.utcnow())
...
2025-01-11 04:05:06

```

Negative values shift time backward:

```python
>>> with immobilus('2025-06-15 12:00:00') as clock:
...     clock.shift(days=-5)
...     print(datetime.utcnow())
...
2025-06-10 12:00:00

```

`shift` can be called multiple times; each call moves the frozen time relative to its current position:

```python
>>> with immobilus('2025-01-01 00:00:00') as clock:
...     clock.shift(seconds=10)
...     print(datetime.utcnow())
...     clock.shift(seconds=20)
...     print(datetime.utcnow())
...
2025-01-01 00:00:10
2025-01-01 00:00:30

```

#### Jumping to a specific time

You can jump the frozen time to an arbitrary point using the `jump` method on the clock object. It accepts either a date string (parsed with `dateutil.parser`) or a `datetime` object:

```python
>>> with immobilus('2025-01-01 00:00:00') as clock:
...     clock.jump('2025-06-15 12:30:00')
...     print(datetime.utcnow())
...
2025-06-15 12:30:00

```

```python
>>> from datetime import datetime
>>> with immobilus('2025-01-01 00:00:00') as clock:
...     clock.jump(datetime(2025, 3, 20, 8, 0, 0))
...     print(datetime.utcnow())
...
2025-03-20 08:00:00

```

Timezone-aware strings and `datetime` objects are automatically converted to UTC:

```python
>>> with immobilus('2025-01-01 00:00:00') as clock:
...     clock.jump('2025-03-20 11:00:00+03:00')
...     print(datetime.utcnow())
...
2025-03-20 08:00:00

```

Unlike `shift`, `jump` sets the frozen time to an absolute value rather than moving it by a relative delta. You can call `jump` multiple times to move between arbitrary points in time:

```python
>>> with immobilus('2025-01-01 00:00:00') as clock:
...     clock.jump('2025-06-01 00:00:00')
...     print(datetime.utcnow())
...     clock.jump(datetime(2025, 12, 31, 23, 59, 59))
...     print(datetime.utcnow())
...
2025-06-01 00:00:00
2025-12-31 23:59:59

```

#### Using as a pytest marker

If you use pytest, you can freeze time for a test using the `@pytest.mark.immobilus` marker. The marker accepts the same arguments as the `immobilus` context manager: a time string (or `datetime` object), an optional `tz_offset`, and an optional `tick` flag.

```python
import pytest
from datetime import datetime

@pytest.mark.immobilus('2017-10-20')
def test_something():
    assert datetime.now() == datetime(2017, 10, 20)
```

You can also pass `tz_offset` and `tick` as keyword arguments:

```python
@pytest.mark.immobilus('2017-10-20 09:00', tz_offset=3)
def test_with_offset():
    assert datetime.now() == datetime(2017, 10, 20, 12, 0, 0)

@pytest.mark.immobilus('2017-10-20 00:00:00', tick=True)
def test_with_tick():
    assert datetime.now().date() == datetime(2017, 10, 20).date()
```

> ✅ No additional configuration is needed — the marker is registered automatically when `immobilus` is installed.

#### Using as a decorator

As well as being a context manager, `immobilus` is also a decorator:

```python
>>> @immobilus('2017-10-20')
... def test():
...     print(datetime.now())
...
>>> test()
2017-10-20 00:00:00

```

It works even with classes

```python

>>> @immobilus('2017-10-20')
... class Decorated(object):
...     now = datetime.utcnow()
...
...     def first(self):
...         return datetime.utcnow()
...     
...     def second(self):
...         return self.now
...
>>> d = Decorated()
>>> assert d.first().strftime('%Y-%m-%d %H:%M:%S') == '2017-10-20 00:00:00'
>>> assert d.second().strftime('%Y-%m-%d %H:%M:%S') != '2017-10-20 00:00:00'

```

and coroutines

```python
>>> import asyncio
>>> 
>>> @immobilus('2017-10-20')
... async def test():
...     return datetime.now()
...
>>> loop = asyncio.new_event_loop()
>>> result = loop.run_until_complete(test())
>>> 
>>> assert result.strftime('%Y-%m-%d %H:%M:%S') == '2017-10-20 00:00:00'

```

#### Using directly

Or you can activate and deactivate `immobilus` manually.

```python
>>> freeze_time = datetime(2017, 10, 20)
>>> spell = immobilus(freeze_time)
>>> datetime.utcnow() == freeze_time
False
>>> spell.start()
FakeDatetime(2017, 10, 20, 0, 0)
>>> datetime.utcnow() == freeze_time
True
>>> datetime.utcnow()
FakeDatetime(2017, 10, 20, 0, 0)
>>> spell.stop()
>>> datetime.utcnow() == freeze_time
False

```

This can be quite useful for those using the standard library `unittest.TestCase` e.g.

```python
import unittest

class SomeTests(unittest.TestCase):
    def setUp(self):
        spell = immobilus('2017-10-20')
        spell.start()
        self.addCleanup(spell.stop)
```

#### Nesting

You can also nest context managers (or decorators, or direct invocations, or any combination) if you want to freeze different times.

```python
>>> with immobilus('2017-10-20 12:00'):
...     print('outer now:    %s' % datetime.now())
...     print('outer utcnow: %s' % datetime.utcnow())
...     with immobilus('2017-10-21 12:00', tz_offset=5):
...         print('inner now:    %s' % datetime.now())
...         print('inner utcnow: %s' % datetime.utcnow())
...     print('outer now:    %s' % datetime.now())
...     print('outer utcnow: %s' % datetime.utcnow())
...
outer now:    2017-10-20 12:00:00
outer utcnow: 2017-10-20 12:00:00
inner now:    2017-10-21 17:00:00
inner utcnow: 2017-10-21 12:00:00
outer now:    2017-10-20 12:00:00
outer utcnow: 2017-10-20 12:00:00

```

#### Special thanks for contribution:
* Eloi Rivard (https://github.com/azmeuk)
* Day Barr (https://github.com/daybarr)
