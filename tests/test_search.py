# -*- coding: utf-8 -*-
"""trakt.sync functional tests"""
import pytest
from trakt.movies import Movie
from trakt.people import Person
from trakt.sync import search, search_by_id
from trakt.tv import TVEpisode, TVShow

__author__ = 'Reinier van der Windt'


def test_invalid_searches():
    """test that the proper exceptions are raised when an invalid search or id
    type is provided to a search function
    """
    functions = [search, search_by_id]
    for fn in functions:
        with pytest.raises(ValueError):
            fn('shouldfail', 'fake')


def test_search_movie():
    """test that movie search results are successfully returned"""
    batman_results = search('batman')
    assert isinstance(batman_results, list)
    assert len(batman_results) == 2
    assert all(isinstance(m, Movie) for m in batman_results)

def test_search_movie_with_year():
    batman_results = search('batman', year='1966')
    assert isinstance(batman_results, list)
    assert len(batman_results) == 1
    assert all(isinstance(m, Movie) for m in batman_results)


def test_search_show():
    """test that tv show search results are successfully returned"""
    batman_results = search('batman', search_type='show')
    assert isinstance(batman_results, list)
    assert all(isinstance(m, TVShow) for m in batman_results)


def test_search_episode():
    """test that tv episode search results are successfully returned"""
    batman_results = search('batman', search_type='episode')
    assert isinstance(batman_results, list)
    assert all(isinstance(m, TVEpisode) for m in batman_results)


def test_search_person():
    """test that person search results are successfully returned"""
    cranston_results = search('cranston', search_type='person')
    assert isinstance(cranston_results, list)
    assert all(isinstance(p, Person) for p in cranston_results)


def test_search_movie_by_id():
    """test that movie by id search results are successfully returned"""
    results = search_by_id('tt0372784', id_type='imdb')
    assert isinstance(results, list)
    assert all(isinstance(m, Movie) for m in results)


def test_search_show_by_id():
    """test that tv show by id search results are successfully returned"""
    results = search_by_id('tt0372784', id_type='imdb')
    assert isinstance(results, list)


def test_search_episode_by_id():
    """test that tv episode by id search results are successfully returned"""
    results = search_by_id('28585', id_type='tmdb')
    assert isinstance(results, list)
    assert len(results) == 3


def test_search_person_by_id():
    """test that person by id search results are successfully returned"""
    results = search_by_id('nm0186505', id_type='imdb')
    assert isinstance(results, list)
    assert all(isinstance(p, Person) for p in results)
