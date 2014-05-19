"""Interfaces to all of the Movie objects offered by the Trakt.tv API"""
import json
import string
import requests
from datetime import datetime, timedelta

from . import api_key, BaseAPI
__author__ = 'Jon Nappi'
__all__ = ['Movie', 'trending_movies', 'updated_movies']


def trending_movies():
    """All :class:`Movie`'s being watched right now"""
    url = BaseAPI().base_url + '/movies/trending.json/{}'.format(api_key)
    response = requests.get(url)
    data = json.loads(response.content.decode('UTF-8'))
    to_ret = []
    for movie in data:
        title = movie.get('title')
        to_ret.append(Movie(title, **movie))
    return to_ret


def updated_movies(timestamp=None):
    """Returns all movies updated since a timestamp. The server time is in PST.
    To establish a baseline timestamp, you can use the server/time method. It's
    recommended to store the timestamp so you can be efficient in using this
    method.
    """
    y_day = datetime.now() - timedelta(1)
    ts = timestamp or int(y_day.strftime('%s')) * 1000
    url = BaseAPI().base_url + '/movies/updated.json/{}/{}'.format(api_key, ts)
    response = requests.get(url)
    data = json.loads(response.content.decode('UTF-8'))
    return data['movies']


class Movie(BaseAPI):
    """A Class representing a Movie object"""
    def __init__(self, title, year=None, **kwargs):
        super(Movie, self).__init__()
        self.title = title
        self.year = int(year)
        self.released_iso = None
        self.url_extension = 'search/movies/' + api_key + '?query='
        if len(kwargs) > 0:
            for key, val in kwargs.items():
                setattr(self, key, val)
        else:
            self.search(self.title)

    def search(self, title):
        query = string.replace(title, ' ', '%20')
        url = self.base_url + self.url_extension + query
        response = requests.get(url)
        data = None
        if response.status_code == 200:
            data = json.loads(response.content)
            if data is not None and self.year is not None:
                for movie in data:
                    title = movie['title'].lower()
                    # print title, self.title.lower()
                    # print movie['year'], self.year, movie['year'] == self.year
                    if movie['year'] == self.year and title == self.title.lower():
                        data = movie
                        break
                if isinstance(data, list):
                    data = data[0]
            elif data is not None and self.year is None:
                data = data[0]
            # print data
            if data is not None and data != []:
                for key, val in data.items():
                    setattr(self, key, val)
            try:
                release = getattr(self, 'released')
                release = float(release)
                utc = datetime.utcfromtimestamp(release)
                self.released_iso = str(utc).replace(' ', 'T')
            except AttributeError:
                pass
