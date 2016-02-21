import json
import os
import pytest
import trakt

MOCK_DATA_DIR = os.path.abspath('tests/mock_data')


MOCK_DATA_FILES = [
    os.path.join(MOCK_DATA_DIR, 'calendars.json')
]


class MockCore(trakt.core.Core):
    def __init__(self, *args, **kwargs):
        super(MockCore, self).__init__(*args, **kwargs)
        self.mock_data = {}
        for mock_file in MOCK_DATA_FILES:
            with open(mock_file) as f:
                self.mock_data.update(json.load(f))

    def _handle_request(self, method, url, data=None):
        uri = url[len(trakt.core.BASE_URL):]
        method_responses = self.mock_data.get(uri, {})
        return method_responses.get(method.upper())


@pytest.fixture()
def mock_core():
    """Override utility functions from trakt.core to use an underlying MockCore
    instance
    """
    trakt.core.CORE = MockCore()
    trakt.core.get = trakt.core.CORE.get
    trakt.core.post = trakt.core.CORE.post
    trakt.core.delete = trakt.core.CORE.delete
    trakt.core.put = trakt.core.CORE.put
    return trakt.core.Core

trakt.core.CORE = MockCore()
trakt.core.get = trakt.core.CORE.get
trakt.core.post = trakt.core.CORE.post
trakt.core.delete = trakt.core.CORE.delete
trakt.core.put = trakt.core.CORE.put
