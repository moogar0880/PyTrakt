"""trakt.users functional tests"""
import os
import unittest

import trakt
from trakt.users import User

__author__ = 'Jon Nappi'


def setUpModule():
    """Convenience setUpModule so we only need to assign the API key once"""
    trakt.api_key = os.environ['TRAKT_TEST_KEY']


def tearDownModule():
    """Cleanup the api_key"""
    del trakt.api_key


class UserTests(unittest.TestCase):
    """Test the functionality of a User object"""
    def setUp(self):
        """Grab environment information for validation"""
        self.user = User(os.environ['TRAKT_TEST_USER'])

    def tearDown(self):
        """Clear out everything created in setUp"""
        self.user = None

    def test_calendar(self):
        """Test that the calendar object is returned successfully"""
        calendar = self.user.calendar
        self.assertIsNotNone(calendar)
        self.assertGreater(len(calendar), 0)
