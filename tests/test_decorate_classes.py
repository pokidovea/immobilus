from immobilus import immobilus

from datetime import datetime


@immobilus('2017-01-01')
class TestClassDecoration(object):

    now = datetime.utcnow()

    def test_one(self):
        assert datetime.utcnow() == datetime(2017, 1, 1)

    def test_two(self):
        assert self.now != datetime(2017, 1, 1)
