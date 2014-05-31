"""Interfaces to all of the Calendar objects offered by the Trakt.tv API"""
import sys
from datetime import datetime
if int(sys.version[0]) == 2:
    from urllib import urlencode
elif int(sys.version[0]) == 3:
    from urllib.parse import urlencode

from . import BaseAPI
from .tv import TVEpisode
import trakt
__author__ = 'Jon Nappi'
__all__ = ['Calendar', 'PremiereCalendar', 'ShowCalendar', 'UserCalendar']


def _now_date_format():
    """Get the current day in the format expected by each :class:`Calendar`"""
    now = datetime.now()
    year = now.year
    month = now.month if now.month > 10 else '0{}'.format(now.month)
    day = now.day if now.day > 10 else '0{}'.format(now.day)
    date = int('{}{}{}'.format(year, month, day))
    return date


class Calendar(BaseAPI):
    """Base :class:`Calendar` type serves as a foundation for other Calendar
    types
    """
    def __init__(self, date=None, days=None):
        """Create a new :class:`Calendar` object

        :param date: Start date of this :class:`Calendar` in the format Ymd
            (i.e. 20110421). Defaults to today
        :param days: Number of days for this :class:`Calendar`. Defaults to 7
            days
        """
        super(Calendar, self).__init__()
        self.date = date or _now_date_format()
        self.days = days or 7
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
        url = self.url
        url_args = {'date': self.date, 'days': self.days}
        formatted_url_args = urlencode({x: url_args[x] for x in url_args if
                                        url_args[x] is not None})
        if formatted_url_args != {}:
            url = '/'.join([url, '?', formatted_url_args])
        return url

    def _build(self):
        """Build the calendar"""
        if self.url is not None:
            ext = self._build_uri()
            data_list = self._get_(ext)
            self._episodes = []
            for data in data_list:
                for episode in data['episodes']:
                    show = episode['show']['title']
                    season = episode['episode']['season']
                    ep = episode['episode']['number']
                    ep_data = episode['episode']
                    self._episodes.append(TVEpisode(show, ep, season,
                                                    episode_data=ep_data))


class PremiereCalendar(Calendar):
    """All shows premiering during the time period specified."""
    def __init__(self, *args, **kwargs):
        super(PremiereCalendar, self).__init__(*args, **kwargs)
        self.url = 'calendar/premieres.json/{}'.format(trakt.api_key)
        self._build()


class ShowCalendar(Calendar):
    """TraktTV ShowCalendar"""
    def __init__(self, *args, **kwargs):
        super(ShowCalendar, self).__init__(*args, **kwargs)
        self.url = 'calendar/shows.json/{}'.format(trakt.api_key)
        self._build()


class UserCalendar(Calendar):
    def __init__(self, user_name, *args, **kwargs):
        super(UserCalendar, self).__init__(*args, **kwargs)
        self.user_name = user_name
        self.url = 'user/calendar/shows.json/{}/{}'.format(trakt.api_key,
                                                           self.user_name)
        self._build()
