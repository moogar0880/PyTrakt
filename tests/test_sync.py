"""trakt.sync functional tests"""
from trakt.sync import comment


class FakeMedia(object):
    """Mock media type object to use with mock sync requests"""
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
