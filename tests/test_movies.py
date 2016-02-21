"""tests for the trakt.movies module"""
from trakt.core import Comment, Translation
from trakt.movies import trending_movies, updated_movies, Movie, Release
from trakt.people import Person
from trakt.users import User


def _get_tron():
    """utility function to return the tron movie"""
    return Movie('Tron Legacy', year=2010)


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
    tron = _get_tron()
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
    tron = _get_tron()
    tron_images = tron.images
    assert isinstance(tron_images, dict)


def test_movie_aliases():
    tron = _get_tron()
    assert isinstance(tron.aliases, list)
    assert len(tron.aliases) == 15


def test_movie_releases():
    tron = _get_tron()
    releases = tron.get_releases()
    assert isinstance(releases, list)
    assert len(releases) == 13
    assert isinstance(releases[0], Release)


def test_movie_translations():
    tron = _get_tron()
    translations = tron.get_translations(country_code='es')
    assert isinstance(translations, list)
    assert len(translations) == 3
    assert isinstance(translations[0], Translation)


def test_movie_comments():
    tron = _get_tron()
    assert isinstance(tron.comments, list)
    assert len(tron.comments) == 1
    assert isinstance(tron.comments[0], Comment)


def test_movie_people():
    tron = _get_tron()
    sub_groups = ['people', 'cast', 'crew']
    for group in sub_groups:
        persons = getattr(tron, group)
        assert isinstance(persons, list)
        assert len(persons) >= 1
        assert isinstance(persons[0], Person)
        assert all(isinstance(p, Person) for p in persons)


def test_movie_ratings():
    tron = _get_tron()
    assert isinstance(tron.ratings, dict)


def test_movie_related():
    tron = _get_tron()
    assert isinstance(tron.related, list)
    assert len(tron.related) == 10
    assert isinstance(tron.related[0], Movie)


def test_movie_watching():
    tron = _get_tron()
    watching_now = tron.watching_now
    assert isinstance(watching_now, list)
    assert len(watching_now) == 2
    assert isinstance(watching_now[0], User)
