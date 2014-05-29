"""Test that the appropriate errors are raised when expected"""
import os
import unittest

import trakt
from trakt.errors import InvalidAPIKey, InvalidCredentials
from trakt.users import User

__author__ = 'Jon Nappi'


class TestBadKey(unittest.TestCase):
    """Simple tests to assert the appropriate exceptions are raised when
    expected
    """
    def test_bad_key(self):
        """Test that a InvalidAPIKey Exception is raised"""
        with self.assertRaises(InvalidAPIKey):
            trakt.api_key = 'ASDFASD'
            User(os.environ['TRAKT_TEST_USER'])

    def test_bad_credentials(self):
        """Test that an InvalidCredentials exception is raised when passing bad
        credentials
        """
        with self.assertRaises(InvalidCredentials):
            user = os.environ['TRAKT_TEST_USER'] + 'sdf'
            password = os.environ['TRAKT_TEST_PASS'] + 'aasdff'
            trakt.authenticate(user, password)
