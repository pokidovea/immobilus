# immobilus

[![build](https://secure.travis-ci.org/pokidovea/immobilus.svg?branch=master)](https://travis-ci.org/pokidovea/immobilus)

A simple time freezing tool for python tests. It mocks:
* datetime.date.today()
* datetime.datetime.now()
* datetime.datetime.utcnow()
* datetime.datetime.fromtimestamp()
* time.time()
* time.gmtime()
* time.localtime()
* time.strftime()
* time.mktime()

## Usage
It is necessary to import *immobilus* first time before import of time functions. For example, place `import immobilus` into root `conftest.py` file if you use [pytest](https://pypi.python.org/pypi/pytest). Then you can import it even after datetime imports.

#### As context manager
```python
from immobilus import immobilus
from datetime import datetime


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
```


#### As decorator
```python
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
```

#### Directly
```python
from immobilus import immobilus
from datetime import datetime

def test_start_stop():

    dt = datetime(2016, 1, 1)
    assert datetime.utcnow() != dt

    spell = immobilus('2016-01-01')
    assert datetime.utcnow() != dt

    spell.start()
    assert datetime.utcnow() == dt
    spell.stop()

    assert datetime.utcnow() != dt
```

#### Special thanks for contribution:
* Éloi Rivard (https://github.com/azmeuk) 
* Day Barr (https://github.com/daybarr)
