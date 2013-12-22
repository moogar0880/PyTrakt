#!/usr/bin/env python
"""
A wrapper for the Trakt.tv REST API
"""
import requests
import string
import json
from pprint import PrettyPrinter

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
        self.percentage = rating_data['percentage']
        self.votes = rating_data['votes']
        self.loved = rating_data['loved']
        self.hated = rating_data['hated']

class TraktStats(object):
    """
    """
    def __init__(self, stats_data):
        super(TraktStats, self).__init__()
        self.watchers = stats_data['watchers']
        self.plays = stats_data['plays']
        self.scrobbles = stats_data['scrobbles']
        self.scrobbles_unique = stats_data['scrobbles_unique']
        self.checkins = stats_data['checkins']
        self.checkins_unique = stats_data['checkins_unique']
        self.collection = stats_data['collection']
        self.collection_unique = stats_data['collection_unique']

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
        # summary.json/888dbf16c37694fd8633f0f7e423dfc5/the-walking-dead
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
            self.year = data['year']
            self.url  = data['url']
            self.first_aired = data['first_aired_iso']
            self.country = data['country']
            self.description = data['overview']
            self.runtime = data['runtime']
            self.status = data['status']
            self.network = data['network']
            self.air_day = data['air_day']
            self.air_time = data['air_time']
            self.certification = data['certification']
            self.imdb_id = data['imdb_id']
            self.tvdb_id = data['tvdb_id']
            self.tvrage_id = data['tvrage_id']
            self.last_updated = data['last_updated']
            self.poster = data['poster']
            self.images = data['images']
            self.genres = data['genres']
            self.actors = data['people']['actors']
            self.rating = TraktRating(data['ratings'])
            self.stats = TraktStats(data['stats'])

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
        print 'TVSeason search'
        url = self.base_url + self.url_extension + '/'
        # Need to remove spaces from show title
        title = string.replace(show_title, ' ', '-')
        url += title + '/' + str(season_num)
        response = requests.get(url)
        data = None
        print url
        if response.status_code == 200:
            data = json.loads(response.content)
        if data != None:
            for episode_data in data:
                self.episodes.append(TVEpisode(self.show, self.season, episode_data=episode_data, key=self.key))

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
            self.episode = episode_data['episode']
            self.number = episode_data['number']
            self.tvdb_id = episode_data['tvdb_id']
            self.title = episode_data['title']
            self.overview = episode_data['overview']
            self.first_aired = episode_data['first_aired_iso']
            self.url = episode_data['url']
            self.screen = episode_data['screen']
            self.images = episode_data['images']
            self.ratings = episode_data['ratings']

    def search(self, show, season, episode_num):
        pass

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
        print url
        if response.status_code == 200:
            data = json.loads(response.content)
        if data != None:
            data = data[0]
            self.year = data['year']
            self.released = data['released']
            self.url = data['url']
            self.trailer_url = data['trailer']
            self.runtime = data['runtime']
            self.tagline = data['tagline']
            self.overview = data['overview']
            self.certification = data['certification']
            self.imdb_id = data['imdb_id']
            self.tmdb_id = data['tmdb_id']
            self.images = data['images']
            self.genres = data['genres']
            self.ratings = data['ratings']
