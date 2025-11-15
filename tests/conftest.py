
import pytest
import unittest.mock as mock

class SimpleMocker:
    def __init__(self):
        self._patchers = []

    def patch(self, target, **kwargs):
        am = mock.AsyncMock()
        if 'return_value' in kwargs:
            am.return_value = kwargs.pop('return_value')
        if 'side_effect' in kwargs:
            am.side_effect = kwargs.pop('side_effect')
        p = mock.patch(target, new=am)
        started = p.start()
        self._patchers.append(p)
        return started

    def stopall(self):
        for p in self._patchers:
            try:
                p.stop()
            except Exception:
                pass
        self._patchers.clear()

@pytest.fixture
def mocker():
    m = SimpleMocker()
    yield m
    m.stopall()
