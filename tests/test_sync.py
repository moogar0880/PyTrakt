# -*- coding: utf-8 -*-
"""trakt.sync functional tests"""
from datetime import datetime
from trakt.sync import (comment, rate, add_to_history, add_to_watchlist,
                        remove_from_history, remove_from_watchlist,
                        add_to_collection, remove_from_collection)


class FakeMedia(object):
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
    assert response is None


def test_create_review():
    """verify that a review can be successfully created"""
    response = comment(FakeMedia(), 'This is a new comment', review=True)
    assert response is None


def test_forced_review():
    """verify that a comment is forced as a review if it's length is > 200"""
    response = comment(FakeMedia(), '*' * 201, review=False)
    assert response is None


def test_rating():
    timestamps = [datetime.now(), None]
    for timestamp in timestamps:
        response = rate(FakeMedia(), 10, timestamp)
        assert response is None


def test_add_to_history():
    timestamps = [datetime.now(), None]
    for timestamp in timestamps:
        response = add_to_history(FakeMedia(), timestamp)


def test_oneliners():
    media = FakeMedia()
    functions = [add_to_watchlist, remove_from_history, remove_from_watchlist,
                 add_to_collection, remove_from_collection]
    for fn in functions:
        response = fn(media)
        assert response is None
