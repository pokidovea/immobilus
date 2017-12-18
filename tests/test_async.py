import sys

import six


if sys.version_info[0:2] >= (3, 5):
    six.exec_("""
from immobilus import immobilus

from datetime import datetime

import pytest

@pytest.mark.asyncio
@immobilus('2000-02-01 13:23')
async def test_decorated_async_function():
    assert datetime.utcnow() == datetime(2000, 2, 1, 13, 23)


@pytest.mark.asyncio
async def test_decorated_async_function():
    dt = datetime(2016, 1, 1, 13, 54)
    assert datetime.utcnow() != dt

    with immobilus('2016-01-01 13:54'):
        assert datetime.utcnow() == dt

    assert datetime.utcnow() != dt
""")
