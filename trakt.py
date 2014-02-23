#!/usr/bin/env python
"""A wrapper for the Trakt.tv REST API"""
import requests
import string
import json
from urllib import urlencode
from pprint import pprint

api_key = None


def configure(key):
    """Configure a session key for use across the entire module"""
    globals()['api_key'] = key


def format_url(url, queries=None):
    """Format the provided url and append urlencoded queries to the end if any
    were provided

    :param url:
    :param queries:
    :return: The formatted
    """
    table = string.maketrans('', '')
    # formatted_url = url.translate(table, string.punctuation)
    formatted_url = ''
    if queries:
        formatted_url += urlencode(queries)
    return formatted_url


class BaseAPI(object):
    """Base class containing all basic functionality of a Trakt.tv API call"""
    def __init__(self):
        super(BaseAPI, self).__init__()
        self.base_url = 'http://api.trakt.tv/'


class TraktRating(object):
    """An object containing data corresponding to the rating information for a
    Trakt show
    """
    def __init__(self, rating_data):
        super(TraktRating, self).__init__()
        for key, val in rating_data.items():
            setattr(self, key, val)


class TraktStats(object):
    """Trakt Statistics object"""
    def __init__(self, stats_data):
        super(TraktStats, self).__init__()
        for key, val in stats_data.items():
            setattr(self, key, val)


class TVShow(BaseAPI):
    """A Class representing a TV Show object
    TODO: library
          watching
          episode/library
          episode/seen
          episode/unlibrary
          episode/unseen
          episode/watchingnow
    """
    def __init__(self, title=''):
        super(TVShow, self).__init__()
        self.url = self.base_url + 'show/'
        self.top_watchers = None
        self.top_episodes = None
        self.seasons = []
        self.title = title
        self.search(show_title=self.title)

    def cancel_watching(self):
        """Cancel watching the current show"""
        url = self.url + 'cancelwatching/' + api_key
        response = requests.get(url)
        if response.status_code == 200:
            pass

    def scrobble(self):
        """Scrobble the current show"""
        url = self.url + 'scrobble/' + api_key
        response = requests.get(url)
        if response.status_code == 200:
            pass

    def watching_now(self):
        """Returns a list of users currently watching this show"""
        url = self.url + 'watchingnow.json/' + api_key + '/' + self.title
        response = requests.get(url)
        if response.status_code == 200:
            pass

    def add_to_library(self):
        """Add this show to your library"""
        pass

    def __fetch_top_watchers(self):
        show_title = self.title
        show_title = string.replace(show_title, ' ', '-')
        url = self.url + 'summary.json/' + api_key + '/' + show_title
        response = requests.get(url)
        if response.status_code == 200:
            data = json.loads(response.content)
            if data is not None:
                self.top_watchers = data['top_watchers']
        return self.top_watchers or None

    def get_top_watchers(self):
        if self.top_watchers is not None:
            return self.top_watchers
        return self.__fetch_top_watchers()

    def __fetch_top_episodes(self):
        show_title = self.title
        show_title = string.replace(show_title, ' ', '-').lower()
        url = self.url + 'summary.json/' + api_key + '/' + show_title
        response = requests.get(url)
        if response.status_code == 200:
            data = json.loads(response.content)
            if data is not None:
                self.top_episodes = data['top_episodes']
        return self.top_episodes

    def get_top_episodes(self):
        if self.top_episodes is not None:
            return self.top_episodes
        return self.__fetch_top_episodes()

    def search(self, show_title=None):
        """Search for general information on a show"""
        show_title = string.replace(show_title, ' ', '-').lower()
        url = self.url + 'summary.json/' + api_key + '/' + show_title
        response = requests.get(url)
        data = None
        if response.status_code == 200:
            data = json.loads(response.content)
        if data is not None:
            for key, val in data.items():
                if key == 'ratings':
                    setattr(self, 'rating', TraktRating(val))
                elif key == 'stats':
                    setattr(self, 'stats', TraktStats(val))
                else:
                    setattr(self, key, val)

    def search_season(self, season_num=None):
        """Search for a show in the Trakt.tv API and store all seasons for this
        show
        """
        try:
            self.seasons[season_num] = TVSeason(self.title, season_num)
        except IndexError:
            while len(self.seasons) < season_num + 1:
                self.seasons.append(None)
            self.seasons[season_num] = TVSeason(self.title, season_num)
        return self.seasons[season_num] or None

    def get_season(self, season_num):
        """Get the requested season"""
        if season_num < 0 or season_num >= len(self.seasons):
            raise Exception
        return self.seasons[season_num-1]


class TVSeason(BaseAPI):
    """Container for TV Seasons"""
    def __init__(self, show, season=1):
        super(TVSeason, self).__init__()
        self.show = show
        self.season = season
        self.episodes = []
        self.url_extension = 'show/season.json/' + api_key
        self.episodes = []
        self.search(self.show, self.season)

    def search(self, show_title, season_num):
        """Search for a tv season"""
        url = self.base_url + self.url_extension + '/'
        # Need to remove spaces and parentheses from show title
        title = string.replace(show_title, ' ', '-').lower()
        title = string.replace(title, '(', '')
        title = string.replace(title, ')', '')
        url += title + '/' + str(season_num)
        response = requests.get(url)
        data = None
        if response.status_code == 200:
            data = json.loads(response.content)
        if data is not None:
            for episode_data in data:
                self.episodes.append(TVEpisode(self.show, self.season,
                                               episode_data=episode_data))

    def __repr__(self):
        title = [self.show, 'Season', self.season]
        title = map(str, title)
        return ' '.join(title)


class TVEpisode(BaseAPI):
    """Container for TV Episodes"""
    def __init__(self, show, season, episode_num=-1, episode_data={}):
        super(TVEpisode, self).__init__()
        self.show = show
        self.season = season
        self.episode = episode_num
        self.overview = self.episode = self.title = None
        if episode_data == {} and episode_num == -1:
            # Do nothing, not enough info given
            pass
        elif episode_num != -1 and episode_data == {}:
            self.search(self.show, self.season, self.episode)
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
    """A Class representing a Movie object"""
    def __init__(self, title):
        super(Movie, self).__init__()
        self.title = title
        self.url_extension = 'search/movies/' + api_key + '?query='
        self.search(self.title)

    def search(self, title):
        query = string.replace(title, ' ', '%20')
        url = self.base_url + self.url_extension + query
        response = requests.get(url)
        data = None
        if response.status_code == 200:
            data = json.loads(response.content)
        if data is not None:
            data = data[0]
            for key, val in data.items():
                setattr(self, key, val)


class Calendar(BaseAPI):
    """TraktTV Calendar"""
    def __init__(self):
        super(Calendar, self).__init__()


class Community(BaseAPI):
    """TraktTV Community Report"""
    def __init__(self, search_type='all', start=None, end=None):
        super(Community, self).__init__()
        self.url_extension = 'community.json/' + api_key + '/' + search_type
        if start is not None and end is None:
            self.url_extension += '/' + str(start)
        elif start is None and end is not None:
            self.url_extension += '/' + str(end)
        else:
            self.url_extension += '/' + str(start) + '/' + str(end)
        url = self.base_url + self.url_extension
        response = requests.get(url)
        data = json.loads(response.content)
        for key, val in data.items():
            setattr(self, key, val)

if __name__ == '__main__':
    my_api_key = '888dbf16c37694fd8633f0f7e423dfc5'
    configure(my_api_key)
    # sea = TVShow('Shameless US').search_season(3)
    # sea = TVShow('Gundam Wing').search_season(1)
    sea = TVShow('House of Cards 2013').search_season(2)
    for ep in sea.episodes:
        pprint(ep.__dict__)
