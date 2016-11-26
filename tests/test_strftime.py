from immobilus import immobilus

import time
from datetime import datetime


def test_ignore_immobilus_when_t_is_set():
    dt = datetime(2016, 1, 1, 14, 56, 13)

    with immobilus('2015-11-16 21:35:16'):
        assert time.strftime('%Y.%m.%d %H/%M/%S', dt.timetuple()) == '2016.01.01 14/56/13'


def test_t_is_not_set():
    with immobilus('2015-11-16 21:35:16'):
        assert time.strftime('%Y.%m.%d %H/%M/%S') == '2015.11.16 21/35/16'
