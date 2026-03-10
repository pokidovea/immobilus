import sys
from datetime import datetime, timezone


def utcnow():
    if sys.version_info >= (3, 12):
        return datetime.now(timezone.utc).replace(tzinfo=None)
    return datetime.utcnow()
