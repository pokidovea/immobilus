import sys

if 'datetime' in sys.modules:
    raise RuntimeError(
        'immobilus must be imported before datetime. '
        'Please ensure that `import immobilus` comes before any imports of `datetime` or modules that import it.'
    )

from immobilus.logic import immobilus


__all__ = ['immobilus']
