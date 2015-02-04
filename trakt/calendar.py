"""Interfaces to all of the Calendar objects offered by the Trakt.tv API"""
from . import BaseAPI
from .tv import TVEpisode
from .utils import now, airs_date

__author__ = 'Jon Nappi'
__all__ = ['Calendar', 'PremiereCalendar', 'ShowCalendar', 'SeasonCalendar',
           'MovieCalendar']


class Calendar(BaseAPI):
    """Base :class:`Calendar` type serves as a foundation for other Calendar
    types
    """

    def __init__(self, date=None, days=7):
        """Create a new :class:`Calendar` object

        :param date: Start date of this :class:`Calendar` in the format Ymd
            (i.e. 20110421). Defaults to today
        :param days: Number of days for this :class:`Calendar`. Defaults to 7
            days
        """
        super(Calendar, self).__init__()
        self.date = date or now()
        self.days = days
        self.url = None
        self._episodes = []

    def __iter__(self):
        """Custom iterator for iterating over the episodes in this Calendar"""
        return iter(self._episodes)

    def __len__(self):
        """Returns the length of the episodes list in this calendar"""
        return len(self._episodes)

    def __str__(self):
        """str representation of this Calendar"""
        from pprint import pformat
        return pformat(self._episodes)
    __repr__ = __str__

    def _build_uri(self):
        """construct the fully formatted url for this Calendar"""
        return '/'.join([self.url, str(self.date), str(self.days)])

    def _build(self):
        """Build the calendar"""
        if self.url is not None:
            ext = self._build_uri()
            data_dict = self._get_(ext)
            self._episodes = []
            for date in data_dict:
                episodes = data_dict.get(date, [])
                for episode in episodes:
                    show = episode.get('show', {}).get('title')
                    season = episode.get('episode', {}).get('season')
                    ep = episode.get('episode', {}).get('number')
                    data = {'airs_at': airs_date(episode.get('airs_at')),
                            'episode_ids': episode.get('episode').get('ids'),
                            'title': episode.get('episode', {}).get('title')}
                    self._episodes.append(TVEpisode(show, ep, season,
                                                    episode_data=data))
            self._episodes = sorted(self._episodes, key=lambda x: x.airs_at)


class PremiereCalendar(Calendar):
    """All shows premiering during the time period specified."""

    def __init__(self, date=None, days=7):
        super(PremiereCalendar, self).__init__(date=date, days=days)
        self.url = 'calendars/shows/new'
        self._build()


class ShowCalendar(Calendar):
    """TraktTV ShowCalendar"""

    def __init__(self, date=None, days=7):
        super(ShowCalendar, self).__init__(date=date, days=days)
        self.url = 'calendars/shows'
        self._build()


class SeasonCalendar(Calendar):
    """TraktTV TV Show Season Premiere"""

    def __init__(self, date=None, days=7):
        super(SeasonCalendar, self).__init__(date=date, days=days)
        self.url = 'calendars/shows/premieres'
        self._build()


class MovieCalendar(Calendar):
    """TraktTV Movie Calendar"""

    def __init__(self, date=None, days=7):
        super(MovieCalendar, self).__init__(date=date, days=days)
        self.url = 'calendars/movies'
        self._build()
