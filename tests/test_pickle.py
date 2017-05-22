import pickle
from immobilus import immobilus
from immobilus.logic import original_datetime

from datetime import datetime


def test_pickle():
    real_datetime = original_datetime.utcnow()
    pickle.dumps(real_datetime)

    with immobilus('1970-01-01'):
        pickle.dumps(datetime.utcnow())

    pickle.dumps(real_datetime)
