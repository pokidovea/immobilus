import pytest

from immobilus.logic import immobilus


def pytest_configure(config):
    config.addinivalue_line(
        'markers',
        'immobilus(time_to_freeze, tz_offset=0, tick=False): freeze time for the test',
    )


@pytest.fixture(autouse=True)
def _immobilus_marker(request):
    marker = request.node.get_closest_marker('immobilus')
    if marker is None:
        yield
        return

    args = marker.args
    kwargs = marker.kwargs
    with immobilus(*args, **kwargs):
        yield
