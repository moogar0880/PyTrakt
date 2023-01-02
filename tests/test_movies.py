# -*- coding: utf-8 -*-
"""tests for the trakt.movies module"""
from trakt.core import Comment
from trakt.movies import (Movie, Release, Translation, dismiss_recommendation,
                          get_recommended_movies, trending_movies,
                          updated_movies)
from trakt.people import Person
from trakt.users import User


def test_trending_movies():
    trending = trending_movies()
    assert isinstance(trending, list)
    assert len(trending) == 2
    assert isinstance(trending[0], Movie)


def test_updated_movies():
    updated = updated_movies('2014-09-22')
    assert isinstance(updated, list)
    assert len(updated) == 2
    assert isinstance(updated[0], Movie)


def test_get_movie():
    tron = Movie('Tron Legacy', year=2010)
    assert isinstance(tron, Movie)
    assert tron.title == 'TRON: Legacy'
    assert tron.year == 2010
    assert tron.tagline == 'The Game Has Changed.'
    assert tron.runtime == 125
    expected = {"trakt": 343,
                "slug": "tron-legacy-2010",
                "imdb": "tt1104001",
                "tmdb": 20526}
    assert tron.ids == {'ids': expected}


def test_get_movie_images():
    tron = Movie('Tron Legacy 2010')
    tron_images = tron.images
    assert isinstance(tron_images, dict)


def test_movie_aliases():
    tron = Movie('Tron Legacy', year=2010)
    assert isinstance(tron.aliases, list)
    assert len(tron.aliases) == 15


def test_movie_releases():
    tron = Movie('Tron Legacy 2010')
    releases = tron.get_releases()
    assert isinstance(releases, list)
    assert len(releases) == 13
    assert isinstance(releases[0], Release)


def test_movie_translations():
    tron = Movie('Tron Legacy', year=2010)
    translations = tron.get_translations(country_code='es')
    assert isinstance(translations, list)
    assert len(translations) == 3
    assert isinstance(translations[0], Translation)


def test_movie_comments():
    tron = Movie('Tron Legacy 2010')
    assert isinstance(tron.comments, list)
    assert len(tron.comments) == 1
    assert isinstance(tron.comments[0], Comment)


def test_movie_people():
    tron = Movie('Tron Legacy', year=2010)
    sub_groups = ['people', 'cast', 'crew']
    for group in sub_groups:
        persons = getattr(tron, group)
        assert isinstance(persons, list)
        assert len(persons) >= 1
        assert isinstance(persons[0], Person)
        assert all(isinstance(p, Person) for p in persons)


def test_movie_ratings():
    tron = Movie('Tron Legacy 2010')
    assert isinstance(tron.ratings, dict)


def test_movie_related():
    tron = Movie('Tron Legacy', year=2010)
    assert isinstance(tron.related, list)
    assert len(tron.related) == 10
    assert isinstance(tron.related[0], Movie)


def test_movie_watching():
    tron = Movie('Tron Legacy 2010')
    watching_now = tron.watching_now
    assert isinstance(watching_now, list)
    assert len(watching_now) == 2
    assert isinstance(watching_now[0], User)


def test_get_recommended_movies():
    recommendations = get_recommended_movies()
    assert isinstance(recommendations, list)
    assert len(recommendations) == 10
    assert all(isinstance(m, Movie) for m in recommendations)


def test_dismiss_movie_recommendation():
    dismissed = dismiss_recommendation(922)
    assert dismissed is None


def test_movie_to_json_singular():
    tron = Movie('Tron Legacy', year=2010)
    expected = {'movie': {'title': tron.title,
                          'year': 2010,
                          'ids': {'imdb': 'tt1104001',
                                  'slug': 'tron-legacy-2010',
                                  'tmdb': 20526,
                                  'trakt': 343}}}
    assert tron.to_json_singular() == expected


def test_movie_to_json():
    tron = Movie('Tron Legacy', year=2010)
    expected = {'movies': [{'title': tron.title,
                            'year': 2010,
                            'ids': {'imdb': 'tt1104001',
                                    'slug': 'tron-legacy-2010',
                                    'tmdb': 20526,
                                    'trakt': 343}}]}
    assert tron.to_json() == expected


def test_movie_str():
    tron = Movie('Tron Legacy 2010')
    assert str(tron) == '<Movie>: {0}'.format(tron.title)
    assert str(tron) == repr(tron)


def test_movie_search():
    results = Movie.search('batman')
    assert isinstance(results, list)
    assert all(isinstance(m, Movie) for m in results)


def test_dismiss():
    tron = Movie('Tron Legacy 2010')
    r = tron.dismiss()
    assert r is None


def test_utilities():
    tron = Movie('Tron Legacy 2010')
    functions = [tron.add_to_library, tron.add_to_collection,
                 tron.add_to_watchlist, tron.mark_as_unseen,
                 tron.remove_from_library, tron.remove_from_collection,
                 tron.remove_from_watchlist, tron.mark_as_seen]
    for fn in functions:
        r = fn()
        assert r is not None


def test_movie_comment():
    tron = Movie('Tron Legacy 2010')
    r = tron.comment('Some comment data')
    assert r is not None


def test_rate_movie():
    tron = Movie('Tron Legacy 2010')
    tron.rate(10)


def test_scrobble_movie():
    tron = Movie('Tron Legacy 2010')
    tron.scrobble(50.0, '1.0.0', '2015-02-01')
