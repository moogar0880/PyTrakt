"""trakt.sync functional tests"""
import os
import unittest
import trakt
from trakt.movies import Movie
from trakt.people import Person
from trakt.sync import search, search_by_id
from trakt.tv import TVEpisode, TVShow

__author__ = 'Reinier van der Windt'


def setUpModule():
    """Convenience setUpModule so we only need to assign the API key once"""
    trakt.api_key = os.environ['TRAKT_TEST_KEY']


def tearDownModule():
    """Cleanup the api_key"""
    del trakt.api_key


class SearchFunctionTests(unittest.TestCase):
    def setUp(self):
        """Grab environment information for validation"""
        self.user_name = os.environ['TRAKT_TEST_USER']
        self.password = os.environ['TRAKT_TEST_PASS']

    def tearDown(self):
        """Clear out everything created in setUp"""
        self.user_name = None
        self.password = None

    def test_search(self):
        """Test that search results are successfully returned"""
        results = search(query='Supergirl', search_type='show')
        self.assertGreaterEqual(len(results), 3)

    def test_search_episode_by_id(self):
        """Test that search results by id are successfully returned"""
        results = search_by_id(query='tt4525842', id_type='imdb')
        self.assertEqual(len(results), 1)
        self.assertIsInstance(results[0], TVEpisode)

    def test_search_show_by_id(self):
        """Test that search results by id are successfully returned"""
        results = search_by_id(query='tt3749900', id_type='imdb')
        self.assertEqual(len(results), 1)
        self.assertIsInstance(results[0], TVShow)

    def test_search_movie_by_id(self):
        """Test that search results by id are successfully returned"""
        results = search_by_id(query='tt2379713', id_type='imdb')
        self.assertEqual(len(results), 1)
        self.assertIsInstance(results[0], Movie)

    def test_search_person_by_id(self):
        """Test that search results by id are successfully returned"""
        results = search_by_id(query='nm0000123', id_type='imdb')
        self.assertEqual(len(results), 1)
        self.assertIsInstance(results[0], Person)
