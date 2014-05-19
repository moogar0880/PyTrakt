"""Interfaces to all of the Calendar objects offered by the Trakt.tv API"""
import sys
import json
import requests
if int(sys.version[0]) == 2:
    from urllib import urlencode
elif int(sys.version[0]) == 3:
    from urllib.parse import urlencode

from . import BaseAPI, api_key
from .tv import TVEpisode
__author__ = 'Jon Nappi'
__all__ = ['Calendar', 'PremiereCalendar', 'ShowCalendar', 'UserCalendar']


class Calendar(BaseAPI):
    def __init__(self, date=None, days=None):
        super(Calendar, self).__init__()
        self.date = date
        self.days = days
        self.url = self.episodes = None

    def _build_url(self):
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
            url = self._build_url()
            response = requests.get(url)
            data_list = json.loads(response.content.decode('UTF-8'))
            self.episodes = []
            for data in data_list:
                for episode in data['episodes']:
                    show = episode['show']['title']
                    season = episode['episode']['season']
                    ep = episode['episode']['number']
                    self.episodes.append(TVEpisode(show, ep, season,
                                                   episode_data=episode['episode']))


class PremiereCalendar(Calendar):
    """All shows premiering during the time period specified."""
    def __init__(self, *args, **kwargs):
        super(PremiereCalendar, self).__init__(*args, **kwargs)
        self.url = self.base_url + '/calendar/premieres.json/' + api_key
        self._build()


class ShowCalendar(Calendar):
    """TraktTV ShowCalendar"""
    def __init__(self, *args, **kwargs):
        super(ShowCalendar, self).__init__(*args, **kwargs)
        self.url = self.base_url + '/calendar/shows.json/' + api_key
        self._build()


class UserCalendar(Calendar):
    def __init__(self, user_name, *args, **kwargs):
        super(UserCalendar, self).__init__(*args, **kwargs)
        self.user_name = user_name
        self.url = '/user/calendar/shows.json/{}/{}'.format(api_key,
                                                            self.user_name)
        self._build()
