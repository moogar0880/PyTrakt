# -*- coding: utf-8 -*-
"""tests for genre retrieval functions"""
from trakt.core import Genre
from trakt.movies import genres as movie_genres
from trakt.tv import genres as tv_genres


def test_genre_functions():
    """test that we can successfully get both movie and tv show genres"""
    for f in [movie_genres, tv_genres]:
        genres = f()
        assert isinstance(genres, list)
        assert len(genres) > 0
        assert all(isinstance(g, Genre) for g in genres)
