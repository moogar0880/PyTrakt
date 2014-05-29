"""trakt.accounts functional tests"""
import os
import unittest

import trakt
from trakt.account import settings, test

__author__ = 'Jon Nappi'


def setUpModule():
    """Convenience setUpModule so we only need to assign the API key once"""
    trakt.api_key = os.environ['TRAKT_TEST_KEY']


def tearDownModule():
    """Cleanup the api_key"""
    del trakt.api_key


class SettingsTest(unittest.TestCase):
    """Pretty basic tests checking that a users settings are appropriately
    returned
    """
    def setUp(self):
        """Grab environment information for validation"""
        self.user_name = os.environ['TRAKT_TEST_USER']
        self.password = os.environ['TRAKT_TEST_PASS']

    def tearDown(self):
        """Clear out everything created in setUp"""
        self.user_name = None
        self.password = None

    def test_settings(self):
        """Test that settings are accurately returned"""
        my_settings = settings(self.user_name, self.password)
        self.assertGreater(len(my_settings), 0)

    def test_settings_type(self):
        """Test that settings are returned as a dict"""
        my_settings = settings(self.user_name, self.password)
        self.assertIsInstance(my_settings, dict)


class AccountTestTest(unittest.TestCase):
    """Assert that accounts are properly validated"""
    def setUp(self):
        """Grab environment information for validation"""
        self.user_name = os.environ['TRAKT_TEST_USER']
        self.password = os.environ['TRAKT_TEST_PASS']

    def tearDown(self):
        """Clear out everything created in setUp"""
        self.user_name = None
        self.password = None

    def test_test_positive(self):
        """Test that a test of a valid account yields a True response"""
        self.assertTrue(test(self.user_name, self.password))

    def test_test_negative(self):
        """Test that a test of an invalid account yields a False response"""
        self.assertFalse(test(self.user_name, self.password))
