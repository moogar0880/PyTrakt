# -*- coding: utf-8 -*-
import pytest

from trakt.people import Credits, MovieCredits, Person, TVCredits


def test_get_person():
    bryan = Person('Bryan Cranston')
    assert bryan.name == 'Bryan Cranston'
    assert bryan.birthday == '1956-03-07'
    assert bryan.death is None
    assert bryan.birthplace == 'San Fernando Valley, California, USA'
    assert bryan.homepage == 'http://www.bryancranston.com/'


def test_get_person_images():
    bryan = Person('Bryan Cranston')
    assert isinstance(bryan.images, dict)


def test_person_magic_methods():
    bryan = Person('Bryan Cranston')
    assert str(bryan) == '<Person>: {name}'.format(name=bryan.name)
    assert str(bryan) == repr(bryan)


def test_person_search():
    results = Person.search('cranston')
    assert len(results) == 10
    assert all(isinstance(p, Person) for p in results)


def test_credits_abc():
    credits = Credits(**{})
    with pytest.raises(NotImplementedError):
        credits._extract_media(None)


def test_get_movie_credits():
    bryan = Person('Bryan Cranston')
    assert isinstance(bryan.movie_credits, MovieCredits)
    assert len(bryan.movie_credits.cast) == 1
    assert len(bryan.movie_credits.crew) == 3

    for job in ('directing', 'writing', 'production'):
        assert job in bryan.movie_credits.crew

def test_get_tv_credits():
    bryan = Person('Bryan Cranston')
    assert isinstance(bryan.tv_credits, TVCredits)
    assert len(bryan.tv_credits.cast) == 1
    assert len(bryan.tv_credits.crew) == 1
    assert 'production' in bryan.tv_credits.crew


def test_credit_magic_methods():
    bryan = Person('Bryan Cranston')
    for credits in (bryan.movie_credits, bryan.tv_credits):
        assert isinstance(credits.cast, list)
        assert isinstance(credits.crew, dict)
        for credit in credits.cast:
            assert str(credit).startswith('<ActingCredit>')
        for department, dep_credits in credits.crew.items():
            for credit in dep_credits:
                assert str(credit).startswith('<CrewCredit>')
