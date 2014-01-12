#!/usr/bin/env python
"""
A wrapper for the Trakt.tv REST API
"""
import requests
import string
import json
from pprint import pprint

class BaseAPI(object):
    """
    Base class containing all basic functionality of a Trakt.tv API call
    """
    def __init__(self, key=None):
        super(BaseAPI, self).__init__()
        self.key = key
        self.base_url = 'http://api.trakt.tv/'

class TraktRating(object):
    """
    An object containing data corresponding to the rating information for a
    Trakt show
    """
    def __init__(self, rating_data):
        super(TraktRating, self).__init__()
        for key, val in rating_data.items():
            setattr(self, key, val)

class TraktStats(object):
    """
    Trakt Statistics object
    """
    def __init__(self, stats_data):
        super(TraktStats, self).__init__()
        for key, val in stats_data.items():
            setattr(self, key, val)

class TVShow(BaseAPI):
    """
    A Class representing a TV Show object
    """
    def __init__(self, title='', *args, **kwargs):
        super(TVShow, self).__init__(*args, **kwargs)
        self.url_extension = 'show/'
        self.top_watchers = None
        self.top_episodes = None
        self.seasons = []
        self.title = title
        self.search(show_title=self.title)

    def __fetch_top_watchers(self):
        show_title = self.title
        string.replace(show_title, ' ', '-')
        url = self.url_extension + 'summary.json/' + self.key + '/'
        url += show_title
        response = requests.get(url)
        data = None
        if response.status_code == 200:
            data = json.loads(response.content)
            if data != None:
                self.top_watchers = data['top_watchers']
        return self.top_watchers

    def get_top_watchers(self):
        if self.top_watchers != None:
            return self.top_watchers
        return self.__fetch_top_watchers()

    def __fetch_top_episodes(self):
        show_title = self.title
        string.replace(show_title, ' ', '-')
        url = self.url_extension + 'summary.json/' + self.key + '/'
        url += show_title
        response = requests.get(url)
        data = None
        if response.status_code == 200:
            data = json.loads(response.content)
            if data != None:
                self.top_episodes = data['top_episodes']
        return self.top_episodes

    def get_top_episodes(self):
        if self.top_episodes != None:
            return self.top_episodes
        return self.__fetch_top_episodes()

    def search(self, show_title=None):
        """
        Search for general information on a show
        """
        url = self.base_url + self.url_extension + 'summary.json/' + self.key + '/'
        # Need to remove spaces from show title
        title = string.replace(show_title, ' ', '-')
        url += title
        response = requests.get(url)
        data = None
        if response.status_code == 200:
            data = json.loads(response.content)
        if data != None:
            for key, val in data.items():
                if key == 'ratings':
                    setattr(self, 'rating', TraktRating(val))
                elif key == 'stats':
                    setattr(self, 'stats', TraktStats(val))
                else:
                    setattr(self, key, val)

    def search_season(self, season_num=None):
        """
        Search for a show in the Trakt.tv API and store all seasons for this
        show
        """
        try:
            self.seasons[season_num] = TVSeason(self.title, season_num, self.key)
        except IndexError:
            while len(self.seasons) < season_num + 1:
                self.seasons.append(None)
            self.seasons[season_num] = TVSeason(self.title, season_num, self.key)
        return self.seasons[season_num] or None

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
    def __init__(self, show, season=1, *args, **kwargs):
        super(TVSeason, self).__init__(*args, **kwargs)
        self.show = show
        self.season = season
        self.episodes = []
        self.url_extension = 'show/season.json/' + self.key
        self.episodes = []
        self.search(self.show, self.season)

    def search(self, show_title, season_num):
        """
        Search for a tv season
        """
        url = self.base_url + self.url_extension + '/'
        # Need to remove spaces from show title
        title = string.replace(show_title, ' ', '-')
        url += title + '/' + str(season_num)
        response = requests.get(url)
        data = None
        if response.status_code == 200:
            data = json.loads(response.content)
        if data != None:
            for episode_data in data:
                self.episodes.append(TVEpisode(self.show, self.season, episode_data=episode_data, key=self.key))

    def __repr__(self):
        title = [self.show, 'Season', self.season]
        title = map(str, title)
        return ' '.join(title)

class TVEpisode(BaseAPI):
    """
    Container for TV Episodes
    """
    def __init__(self, show, season, episode_num=-1, episode_data={}, *args, **kwargs):
        super(TVEpisode, self).__init__(*args, **kwargs)
        self.show = show
        self.season = season
        if episode_data == {} and episode_num == -1:
            # Do nothing, not enough info given
            pass
        elif episode_num != -1 and episode_data == {}:
            self.search(self.show, self.season, self.episode_num)
        else: # episode_data != {}
            for key, val in episode_data.items():
                setattr(self, key, val)
        # if 'overview' in self.__dict__:
            # self.overview = string.replace(self.overview, u'\u2013', '-')
            # self.overview = string.replace(self.overview, u'\u2019', '\'')
            # self.overview = string.replace(self.overview, u'\u2019', '"')

    def search(self, show, season, episode_num):
        pass

    def get_description(self):
        return str(self.overview)

    def __repr__(self):
        title = [self.episode, self.title]
        title = map(str, title)
        return ' '.join(title)

class Movie(BaseAPI):
    """
    A Class representing a Movie object
    """
    def __init__(self, title, *args, **kwargs):
        super(Movie, self).__init__(*args, **kwargs)
        self.title = title
        self.url_extension = 'search/movies/' + self.key + '?query='
        self.search(self.title)

    def search(self, title):
        query = string.replace(title, ' ', '%20')
        url = self.base_url + self.url_extension + query
        response = requests.get(url)
        data = None
        if response.status_code == 200:
            data = json.loads(response.content)
        if data != None:
            data = data[0]
            for key, val in data.items():
                setattr(self, key, val)

class Calendar(BaseAPI):
    """
    TraktTV Calendar
    """
    def __init__(self):
        super(Calendar, self).__init__()

class Community(BaseAPI):
    """
    TraktTV Community Report
    """
    def __init__(self, search_type='all', start=None, end=None, *args, **kwargs):
        super(Community, self).__init__(*args, **kwargs)
        self.url_extension = 'community.json/' + self.key + '/' + search_type
        if start is not None and end is None:
            self.url_extension += '/' str(start)
        elif start is None and end is not None:
            self.url_extension += '/' str(end)
        else:
            self.url_extension += '/' str(start) + '/' + str(end)
        url = self.base_url + self.url_extension
        response = requests.get(url)
        data = json.loads(response.content)
        for key, val in data.items():
            setattr(self, key, val)
