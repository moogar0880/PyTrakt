"""trakt.movies functional tests"""
import os
import unittest

import trakt
from trakt import Comment, Genre
from trakt.users import User
import trakt.movies
from trakt.movies import Movie, get_recommended_movies, trending_movies, \
    updated_movies

__author__ = 'Jon Nappi'


def setUpModule():
    """Convenience setUpModule so we only need to assign the API key once"""
    trakt.api_key = os.environ['TRAKT_TEST_KEY']


def tearDownModule():
    """Cleanup the api_key"""
    del trakt.api_key


class MovieTest(unittest.TestCase):
    """Test the functionality of the Movie object"""
    def setUp(self):
        """Grab environment information for validation"""
        self.user_name = os.environ['TRAKT_TEST_USER']
        self.password = os.environ['TRAKT_TEST_PASS']
        trakt.authenticate(self.user_name, self.password)
        self.movie = Movie('Gravity')

    def tearDown(self):
        """Clear out everything created in setUp"""
        self.user_name = None
        self.password = None
        self.movie = None

    def test_comments_length(self):
        """Test the length of the movie's comment list"""
        self.assertGreater(len(self.movie.comments), 0)

    def test_comments_type(self):
        """Test the type of the Movie's comments"""
        self.assertIsInstance(self.movie.comments[0], Comment)

    def test_related_length(self):
        """Test the length of the movie's related list"""
        self.assertGreater(len(self.movie.related), 0)

    def test_related_type(self):
        """Test the type of the Movie's related"""
        self.assertIsInstance(self.movie.related[0], Movie)

    def test_watching_now_length(self):
        """Test the length of the movie's watching now list"""
        self.assertGreater(len(self.movie.watching_now), 0)

    def test_watching_now_type(self):
        """Test the type of a Movie's watching now"""
        self.assertIsInstance(self.movie.watching_now[0], User)


class MovieFunctionTests(unittest.TestCase):
    def setUp(self):
        """Grab environment information for validation"""
        self.user_name = os.environ['TRAKT_TEST_USER']
        self.password = os.environ['TRAKT_TEST_PASS']

    def tearDown(self):
        """Clear out everything created in setUp"""
        self.user_name = None
        self.password = None

    def test_recommendations(self):
        """Test that recommendations are successfully returned"""
        recommendations = get_recommended_movies()
        self.assertGreater(len(recommendations), 0)
        self.assertIsInstance(recommendations[0], Movie)

    def test_genres(self):
        """Test that genres are returned successfully"""
        genres = trakt.movies.genres()
        self.assertGreater(len(genres), 0)
        self.assertIsInstance(genres[0], Genre)

    def test_trending_movies(self):
        """Test that trending movies are returned successfully"""
        movies = trending_movies()
        self.assertGreater(len(movies), 0)
        self.assertIsInstance(movies[0], Movie)

    def test_updated_movies(self):
        """Test that updated movies are returned successfully"""
        movies = updated_movies()
        self.assertGreater(len(movies), 0)
        self.assertIsInstance(movies[0], Movie)
