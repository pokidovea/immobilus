# immobilus

[![Download from PyPI](https://img.shields.io/pypi/v/immobilus.svg)](https://pypi.python.org/pypi/immobilus)
[![build](https://secure.travis-ci.org/pokidovea/immobilus.svg?branch=master)](https://travis-ci.org/pokidovea/immobilus)
[![Build status](https://ci.appveyor.com/api/projects/status/jpidjtu298ason8h?svg=true)](https://ci.appveyor.com/project/pokidovea/immobilus)

A simple time freezing tool for python tests. It mocks:
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
>>> from datetime import datetime

```

For example, if you use [pytest](https://pypi.python.org/pypi/pytest), you could add `import immobilus` into your root `conftest.py` file.

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

and coroutines (since `python 3.5`)

```python
>>> import sys
>>> import six
>>>
>>> if sys.version_info[0:2] >= (3, 5):
...    result = ''
...    six.exec_("""
... import asyncio
...  
... @immobilus('2017-10-20')
... async def test():
...    return datetime.now()
...
... loop = asyncio.new_event_loop()
... result = loop.run_until_complete(test())
...     """)
...    assert result.strftime('%Y-%m-%d %H:%M:%S') == '2017-10-20 00:00:00'

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
