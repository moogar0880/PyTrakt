# -*- coding: utf-8 -*-
import json
import os
from copy import deepcopy
from functools import lru_cache

from requests import Session

import trakt
from trakt.api import HttpClient

TESTS_DIR = os.path.dirname(__file__)
MOCK_DATA_DIR = os.path.join(TESTS_DIR, "mock_data")

MOCK_DATA_FILES = [
    os.path.join(MOCK_DATA_DIR, 'calendars.json'),
    os.path.join(MOCK_DATA_DIR, 'comments.json'),
    os.path.join(MOCK_DATA_DIR, 'genres.json'),
    os.path.join(MOCK_DATA_DIR, 'movies.json'),
    os.path.join(MOCK_DATA_DIR, 'people.json'),
    os.path.join(MOCK_DATA_DIR, 'recommendations.json'),
    os.path.join(MOCK_DATA_DIR, 'scrobble.json'),
    os.path.join(MOCK_DATA_DIR, 'search.json'),
    os.path.join(MOCK_DATA_DIR, 'shows.json'),
    os.path.join(MOCK_DATA_DIR, 'seasons.json'),
    os.path.join(MOCK_DATA_DIR, 'episodes.json'),
    os.path.join(MOCK_DATA_DIR, 'sync.json'),
    os.path.join(MOCK_DATA_DIR, 'users.json'),
]


class MockCore():
    def __init__(self):
        self.mock_data = {}
        for mock_file in MOCK_DATA_FILES:
            with open(mock_file, encoding='utf-8') as f:
                self.mock_data.update(json.load(f))

    def request(self, method, uri, data=None):
        if uri.startswith('/'):
            uri = uri[1:]
        # use a deepcopy of the mocked data to ensure clean responses on every
        # request. this prevents rewrites to JSON responses from persisting
        method_responses = self.mock_data.get(uri, {})
        response = method_responses.get(method.upper())
        if response is None:
            print(f"No mock for {uri}")
        return deepcopy(response)


"""Override request function with MockCore instance
"""

trakt.core.api().request = MockCore().request

trakt.core.CLIENT_ID = 'FOO'
trakt.core.CLIENT_SECRET = 'BAR'
