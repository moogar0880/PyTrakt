# -*- coding: utf-8 -*-
"""trakt.tv functional tests"""
from trakt.core import Comment
from trakt.people import Person
from trakt.tv import (trending_shows, popular_shows, updated_shows, TVShow,
                      dismiss_recommendation, get_recommended_shows)
from trakt.users import User


def test_dismiss_show_recomendation():
    r = dismiss_recommendation(922)
    assert r is None


def test_recommended_shows():
    assert all([isinstance(s, TVShow) for s in get_recommended_shows()])


def test_trending_shows():
    shows = trending_shows()
    assert len(shows) == 2


def test_popular_shows():
    shows = popular_shows()
    assert len(shows) == 10


def test_updated_shows():
    shows = updated_shows('2014-09-22')
    assert len(shows) == 2


def test_get_show():
    titles = ['Game of Thrones', 'game-of-thrones']
    for title in titles:
        got = TVShow(title)
        images = got.images
        assert isinstance(images, dict)
        assert str(got) == '<TVShow> ' + got.title
        assert repr(got) == str(got)


def test_aliases():
    got = TVShow('Game of Thrones')
    assert isinstance(got.aliases, list)


def test_translations():
    got = TVShow('Game of Thrones')
    translations = got.get_translations('es')
    assert isinstance(translations, list)
    assert len(translations) == 3


def test_get_comments():
    got = TVShow('Game of Thrones')
    assert all(isinstance(c, Comment) for c in got.comments)
    assert len(got.comments) == 1


def test_get_people():
    got = TVShow('Game of Thrones')
    assert isinstance(got.people, list)
    groups = [got.people, got.cast, got.crew]
    for group in groups:
        assert all([isinstance(p, Person) for p in group])


def test_ratings():
    got = TVShow('Game of Thrones')
    assert isinstance(got.ratings, dict)


def test_related():
    got = TVShow('Game of Thrones')
    assert all(isinstance(s, TVShow) for s in got.related)


def test_watching():
    got = TVShow('Game of Thrones')
    assert all(isinstance(u, User) for u in got.watching_now)


def test_show_search():
    results = TVShow.search('batman')
    assert isinstance(results, list)
    assert all(isinstance(m, TVShow) for m in results)


def test_show_search_with_year():
    results = TVShow.search('batman', year=1999)
    assert isinstance(results, list)
    assert len(results) == 1
    assert all(isinstance(m, TVShow) for m in results)


def test_show_ids():
    got = TVShow('Game of Thrones')
    assert isinstance(got.ids, dict)


def test_oneliners():
    got = TVShow('Game of Thrones')
    functions = [got.add_to_library, got.add_to_collection,
                 got.add_to_watchlist, got.dismiss, got.mark_as_seen,
                 got.mark_as_unseen, got.remove_from_library,
                 got.remove_from_collection, got.remove_from_watchlist]
    for fn in functions:
        assert fn() is None


def test_show_comment():
    got = TVShow('Game of Thrones')
    got.comment('Test Comment Data')


def test_rate_show():
    got = TVShow('Game of Thrones')
    got.rate(10)
