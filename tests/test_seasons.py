# -*- coding: utf-8 -*-
"""trakt.tv functional tests"""
from trakt.core import Comment
from trakt.tv import TVEpisode, TVSeason, TVShow
from trakt.users import User


def test_get_seasons():
    got = TVShow('Game of Thrones')
    assert all([isinstance(s, TVSeason) for s in got.seasons])
    season = got.seasons[1]
    assert season.season == 1
    assert len(season.episodes) == 10
    assert all([isinstance(episode, TVEpisode) for episode in season.episodes])


def test_get_seasons_with_year():
    got = TVShow('The Flash', year=2014)
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


def test_episodes_getter():
    s1 = TVSeason('Game of Thrones')
    s1._episodes = None
    for _ in range(2):
        assert all([isinstance(e, TVEpisode) for e in s1.episodes])


def test_oneliners():
    s1 = TVSeason('Game of Thrones')
    functions = [s1.add_to_library, s1.add_to_collection,
                 s1.remove_from_library, s1.remove_from_collection]
    for fn in functions:
        r = fn()
        assert r is not None


def test_season_to_json():
    s1 = TVSeason('Game of Thrones')
    assert isinstance(s1.to_json(), dict)


def test_season_magic_methods():
    s1 = TVSeason('Game of Thrones')
    assert str(s1) == '<TVSeason>: %s Season %d' % (s1.show, s1.season)
    assert str(s1) == repr(s1)
    assert len(s1) == len(s1.episodes)
