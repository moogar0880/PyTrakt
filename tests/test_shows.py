"""trakt.tv functional tests"""
from trakt.core import Comment
from trakt.people import Person
from trakt.tv import trending_shows, popular_shows, updated_shows, TVShow
from trakt.users import User


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
    assert all([isinstance(p, Person) for p in got.people])


def test_ratings():
    got = TVShow('Game of Thrones')
    assert isinstance(got.ratings, dict)


def test_related():
    got = TVShow('Game of Thrones')
    assert all(isinstance(s, TVShow) for s in got.related)


def test_watching():
    got = TVShow('Game of Thrones')
    assert all(isinstance(u, User) for u in got.watching_now)
