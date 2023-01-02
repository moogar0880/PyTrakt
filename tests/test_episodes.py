# -*- coding: utf-8 -*-
"""trakt.tv functional tests"""
from trakt.core import Comment
from trakt.sync import Scrobbler
from trakt.tv import TVEpisode, TVSeason
from trakt.users import User
from trakt.utils import airs_date


def test_get_episodes():
    s1 = TVSeason('Game of Thrones', season=1)
    assert all([isinstance(e, TVEpisode) for e in s1.episodes])


def test_episode_search():
    results = TVEpisode.search('batman')
    assert isinstance(results, list)
    assert all(isinstance(m, TVEpisode) for m in results)


def test_episode_search_with_year():
    results = TVEpisode.search('batman', year=1987)
    assert isinstance(results, list)
    assert len(results) == 10
    assert all(isinstance(m, TVEpisode) for m in results)


def test_get_episode():
    e1 = TVEpisode('Game of Thrones', season=1, number=1)
    assert e1.season == 1
    assert e1.number == 1
    assert e1.get_description() == e1.overview


def test_episode_comments():
    e1 = TVEpisode('Game of Thrones', season=1, number=1)
    assert all([isinstance(c, Comment) for c in e1.comments])


def test_episode_ratings():
    e1 = TVEpisode('Game of Thrones', season=1, number=1)
    assert isinstance(e1.ratings, dict)


def test_episode_watching_now():
    e1 = TVEpisode('Game of Thrones', season=1, number=1)
    assert all([isinstance(u, User) for u in e1.watching_now])


def test_episode_images():
    e1 = TVEpisode('Game of Thrones', season=1, number=1)
    for _ in range(2):
        assert isinstance(e1.images, dict)


def test_episode_ids():
    e1 = TVEpisode('Game of Thrones', season=1, number=1)
    assert isinstance(e1.ids, dict)
    assert e1.trakt == e1.ids['ids']['trakt']
    assert e1.imdb == e1.ids['ids']['imdb']
    assert e1.tmdb == e1.ids['ids']['tmdb']


def test_rate_episode():
    e1 = TVEpisode('Game of Thrones', season=1, number=1)
    e1.rate(10)


def test_oneliners():
    e1 = TVEpisode('Game of Thrones', season=1, number=1)

    functions = [e1.add_to_library, e1.add_to_collection, e1.add_to_watchlist,
                 e1.mark_as_seen, e1.mark_as_unseen, e1.remove_from_library,
                 e1.remove_from_collection, e1.remove_from_watchlist]
    for fn in functions:
        r = fn()
        assert r is not None


def test_episode_comment():
    e1 = TVEpisode('Game of Thrones', season=1, number=1)
    r = e1.comment('Test Comment')
    assert r is not None


def test_episode_scrobble():
    e1 = TVEpisode('Game of Thrones', season=1, number=1)
    scrobbler = e1.scrobble(50.0, '1.0.0', '2015-02-07')
    assert isinstance(scrobbler, Scrobbler)


def test_episode_magic_methods():
    e1 = TVEpisode('Game of Thrones', season=1, number=1)
    assert str(e1) == '<TVEpisode>: %s S%dE%d %s' % (e1.show, e1.season,
                                                     e1.number, e1.title)
    assert str(e1) == repr(e1)

def test_episode_aired_dates():
    e1 = TVEpisode('Game of Thrones', season=1, number=1)
    assert e1.first_aired_date == airs_date('2011-04-18T01:00:00.000Z')
    assert e1.first_aired_end_time == airs_date('2011-04-18T01:58:00.000Z')
