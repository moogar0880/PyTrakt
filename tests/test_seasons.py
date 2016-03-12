"""trakt.tv functional tests"""
from trakt.core import Comment
from trakt.tv import TVShow, TVSeason
from trakt.users import User


def test_get_seasons():
    got = TVShow('Game of Thrones')
    assert all([isinstance(s, TVSeason) for s in got.seasons])


def test_get_season():
    s1 = TVSeason('Game of Thrones', season=1)
    assert isinstance(s1, TVSeason)
    assert len(s1) == 10


def test_season_comments():
    s1 = TVSeason('Game of Thrones')
    assert all([isinstance(c, Comment) for c in s1.comments])


def test_season_ratings():
    s1 = TVSeason('Game of Thrones')
    assert isinstance(s1.ratings, dict)


def test_season_watching_now():
    s1 = TVSeason('Game of Thrones')
    assert all([isinstance(u, User) for u in s1.watching_now])
