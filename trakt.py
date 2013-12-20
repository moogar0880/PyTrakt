#!/usr/bin/env python
"""
A wrapper for the Trakt.tv REST API
"""
import requests
import string
import json

class BaseAPI(object):
    """
    Base class containing all basic functionality of a Trakt.tv API call
    """
    def __init__(self, key=None):
        super(BaseAPI, self).__init__()
        self.key = key
        self.base_url = 'http://api.trakt.tv/'

class TVShow(BaseAPI):
    """
    A Class representing a TV Show object
    """
    def __init__(self, *args, **kwargs):
        super(TVShow, self).__init__(*args, **kwargs)
        self.url_extension = 'show/'
        self.description = {}
        self.seasons = []

    def search(self, show_title=None):
        """
        Search for general information on a show
        """
        url = self.base_url + self.url_extension + 'summary.json/' + self.key
        # Need to remove spaces from show title
        string.replace(show_title, ' ', '-')
        url += show_title
        response = requests.get(url)
        data = None
        if response.status_code == 200:
            data = json.loads(response.content)
        if data != None:
            self.title = data['title']

    def search_season(self, show_title=None):
        """
        Search for a show in the Trakt.tv API and store all seasons for this
        show
        """
        if show_title is None:
            return None
        else:
            url = self.base_url + self.url_extension + 'seasons.json/'
            # Append API Key to the URL
            url += self.key + '/'
            # Need to remove spaces from show title
            string.replace(show_title, ' ', '-')
            # And append search criteria to url
            url += show_title
            response = requests.get(url)
            data = None
            if response.status_code == 200:
                data = json.loads(response.content)
            if data != None:
                for season_data in data:
                    self.seasons.append(TVSeason(season_data))

    def get_season(self, season_num):
        """
        Get the requested season
        """
        if season_num < 0 or season_num >= len(self.seasons):
            raise Exception
        return self.seasons[season_num-1]

class TVSeason(BaseAPI):
    """
    Container for TV Seasons
    """
    def __init__(self, dict_contents={}):
        super(TVSeason, self).__init__()
        self.url = dict_contents['url']
        self.season = dict_contents['season']
        self.episodes = dict_contents['episodes']
        self.images = dict_contents['images']
        self.poster = dict_contents['poster']
        self.url_extension = 'show/season.json/' + self.key
        self.episodes = []

    def search(self, show_title, season_num):
        url = self.base_url + self.url_extension + '/'
        # Need to remove spaces from show title
        string.replace(show_title, ' ', '-')
        url += show_title + '/' + str(season_num)
        response = requests.get(url)
        data = None
        if response.status_code == 200:
            data = json.loads(response.content)
        if data != None:
            for episode_data in data:
                self.episodes.append(TVEpisode(episode_data))

class TVEpisode(BaseAPI):
    """
    Container for TV Episodes
    """
    def __init__(self, arg):
        super(TVEpisode, self).__init__()
        self.arg = arg







