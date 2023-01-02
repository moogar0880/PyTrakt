# -*- coding: utf-8 -*-
"""trakt.sync functional tests"""
from trakt.movies import Movie
from trakt.people import Person
from trakt.sync import SearchResult, get_search_results, search, search_by_id
from trakt.tv import TVEpisode, TVShow

__author__ = 'Reinier van der Windt'


def test_search_movie():
    """test that movie search results are successfully returned"""
    batman_results = search('batman')
    assert isinstance(batman_results, list)
    assert len(batman_results) == 2
    assert all(isinstance(m, Movie) for m in batman_results)


def test_search_movie_with_year():
    batman_results = search('batman', year='1966')
    assert isinstance(batman_results, list)
    assert len(batman_results) == 2
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


def test_search_show_by_id_with_explicit_type():
    """test that tv show by id search results are successfully returned when
    explicitly adding the media type"""
    results = search_by_id('78845', id_type='tvdb', media_type='show')
    assert isinstance(results, list)


def test_search_by_id_with_multiple_results():
    """test that searching by id search results are successfully returned when
    there are multiple types"""
    results = search_by_id('78845', id_type='tvdb', media_type='show')
    assert isinstance(results, list)


def test_get_search_results():
    """test that entire results can be returned by get_search_results"""
    results = get_search_results('batman', search_type=['movie'])
    assert isinstance(results, list)
    assert len(results) == 2
    assert all(isinstance(r, SearchResult) for r in results)
    assert all([r.score != 0.0 for r in results])
