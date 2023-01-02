# -*- coding: utf-8 -*-
"""trakt.sync functional tests"""
from datetime import datetime

import pytest

from trakt.sync import (add_to_collection, add_to_history, add_to_watchlist,
                        comment, rate, remove_from_collection,
                        remove_from_history, remove_from_watchlist)


class FakeMedia:
    """Mock media type object to use with mock sync requests"""
    media_type = 'fake'

    def __init__(self):
        self.ids = {}

    def to_json_singular(self):
        return {}

    def to_json(self):
        return {}


def test_create_comment():
    """test comment creation"""
    response = comment(FakeMedia(), 'This is a new comment', spoiler=True)
    assert response.get('comment')


def test_create_review():
    """verify that a review can be successfully created"""
    response = comment(FakeMedia(), 'This is a new comment', review=True)
    assert response.get('comment')


def test_forced_review():
    """verify that a comment is forced as a review if it's length is > 200"""
    response = comment(FakeMedia(), '*' * 201, review=False)
    assert response.get('comment')


def test_rating():
    timestamps = [datetime.now(), None]
    for timestamp in timestamps:
        response = rate(FakeMedia(), 10, timestamp)
        assert response['added'] == {
            'episodes': 2, 'movies': 1, 'seasons': 1, 'shows': 1
        }
        assert len(response['not_found']['movies']) == 1


def test_add_to_history():
    timestamps = [datetime.now(), None]
    for timestamp in timestamps:
        response = add_to_history(FakeMedia(), timestamp)


@pytest.mark.parametrize('fn,get_key', [
        (add_to_watchlist, 'added'),
        (remove_from_history, 'deleted'),
        (remove_from_watchlist, 'deleted'),
        (add_to_collection, 'added'),
        (remove_from_collection, 'deleted')
    ]
)
def test_oneliners(fn, get_key):
    media = FakeMedia()
    response = fn(media)
    assert response.get(get_key)
