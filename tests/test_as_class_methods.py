# https://github.com/pokidovea/immobilus/issues/30

from immobilus import immobilus  # noqa
from immobilus.logic import fake_time, fake_localtime, fake_gmtime, fake_strftime, fake_mktime

from datetime import datetime


class SomeClass(object):
    method = None


def test_fake_time():
    SomeClass.method = fake_time

    instance = SomeClass()
    instance.method()


def test_fake_localtime():
    SomeClass.method = fake_localtime

    instance = SomeClass()
    instance.method(12345)


def test_fake_gmtime():
    SomeClass.method = fake_gmtime

    instance = SomeClass()
    instance.method(12345)


def test_fake_strftime():
    SomeClass.method = fake_strftime

    instance = SomeClass()
    instance.method('%H:%M')


def test_fake_mktime():
    SomeClass.method = fake_mktime

    timetuple = datetime.utcnow().timetuple()

    instance = SomeClass()
    instance.method(timetuple)
