"""trakt.tv functional tests"""
from trakt.core import Comment
from trakt.tv import TVSeason, TVEpisode
from trakt.users import User


def test_get_episodes():
    s1 = TVSeason('Game of Thrones', season=1)
    assert all([isinstance(e, TVEpisode) for e in s1.episodes])


def test_get_episode():
    e1 = TVEpisode('Game of Thrones', season=1, number=1)
    assert e1.season == 1
    assert e1.number == 1


def test_episode_comments():
    e1 = TVEpisode('Game of Thrones', season=1, number=1)
    assert all([isinstance(c, Comment) for c in e1.comments])


def test_episode_ratings():
    e1 = TVEpisode('Game of Thrones', season=1, number=1)
    assert isinstance(e1.ratings, dict)


def test_episode_watching_now():
    e1 = TVEpisode('Game of Thrones', season=1, number=1)
    assert all([isinstance(u, User) for u in e1.watching_now])
