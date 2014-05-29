"""trakt.people functional tests"""
import os
import unittest

import trakt
from trakt.people import Person

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
        self.actor = Person('Christian Bale')

    def tearDown(self):
        """Clear out everything created in setUp"""
        self.actor = None

    def test_actor_built(self):
        """Test the all fields in the Person class were set"""
        self.assertIsNotNone(self.actor.bio)
        self.assertIsNotNone(self.actor.birthplace)
        self.assertIsNotNone(self.actor.tmdb_id)
        self.assertIsNotNone(self.actor.birthday)
        self.assertGreater(len(self.actor.images), 0)
