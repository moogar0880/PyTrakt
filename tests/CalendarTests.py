"""trakt.calendar functional tests"""
import os
import unittest

import trakt
from trakt.calendar import PremiereCalendar, ShowCalendar, UserCalendar

__author__ = 'Jon Nappi'


def setUpModule():
    """Convenience setUpModule so we only need to assign the API key once"""
    trakt.api_key = os.environ['TRAKT_TEST_KEY']


def tearDownModule():
    """Cleanup the api_key"""
    del trakt.api_key


class PremiereCalendarTest(unittest.TestCase):
    """Tests the functionality of the PremiereCalendar"""
    def setUp(self):
        """Create a PremiereCalendar and hold onto it"""
        self.calendar = PremiereCalendar()

    def tearDown(self):
        """Wipe out the calendar between tests"""
        self.calendar = None

    def test_calendar_type(self):
        """Assert that we get a Calendar object back, not a dict"""
        self.assertIsInstance(self.calendar, PremiereCalendar)

    def test_calendar_date(self):
        """Assert that the correct start date is stored in the calendar"""
        self.assertGreater(self.calendar.date, 20140000)

    def test_calendar_days(self):
        """Assert that the corrent length of time is stored in the calendar"""
        self.assertEqual(self.calendar.days, 7)

    def test_calendar_length(self):
        """Assert that the length of the calendar is greater than zero"""
        self.assertGreater(len(self.calendar), 0)


class ShowCalendarTest(unittest.TestCase):
    """Tests the functionality of the ShowCalendar"""
    def setUp(self):
        """Create a PremiereCalendar and hold onto it"""
        self.calendar = ShowCalendar()

    def tearDown(self):
        """Wipe out the calendar between tests"""
        self.calendar = None

    def test_calendar_type(self):
        """Assert that we get a Calendar object back, not a dict"""
        self.assertIsInstance(self.calendar, ShowCalendar)

    def test_calendar_date(self):
        """Assert that the correct start date is stored in the calendar"""
        self.assertGreater(self.calendar.date, 20140000)

    def test_calendar_days(self):
        """Assert that the corrent length of time is stored in the calendar"""
        self.assertEqual(self.calendar.days, 7)

    def test_calendar_length(self):
        """Assert that the length of the calendar is greater than zero"""
        self.assertGreater(len(self.calendar), 0)


class UserCalendarTest(unittest.TestCase):
    """Tests the functionality of the UserCalendar"""
    def setUp(self):
        """Create a PremiereCalendar and hold onto it"""
        self.user_name = os.environ['TRAKT_TEST_USER']
        self.calendar = UserCalendar(self.user_name)

    def tearDown(self):
        """Wipe out the calendar between tests"""
        self.calendar = None

    def test_calendar_type(self):
        """Assert that we get a Calendar object back, not a dict"""
        self.assertIsInstance(self.calendar, UserCalendar)

    def test_calendar_date(self):
        """Assert that the correct start date is stored in the calendar"""
        self.assertGreater(self.calendar.date, 20140000)

    def test_calendar_days(self):
        """Assert that the corrent length of time is stored in the calendar"""
        self.assertEqual(self.calendar.days, 7)

    def test_calendar_length(self):
        """Assert that the length of the calendar is greater than zero"""
        self.assertGreater(len(self.calendar), 0)

    def test_calendar_user_name(self):
        """Assert that the length of the calendar is greater than zero"""
        self.assertEqual(self.user_name, self.calendar.user_name)
