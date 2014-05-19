"""Interfaces to all of the People objects offered by the Trakt.tv API"""
import json
import requests

from . import api_key, BaseAPI
__author__ = 'Jon Nappi'
__all__ = ['Person']


class Person(BaseAPI):
    """A Class representing a Movie object"""
    def __init__(self, name, **kwargs):
        super(Person, self).__init__()
        self.name = name
        self.url = self.biography = self.birthplace = self.tmdb_id = None
        self.images = []
        self.url_extension = 'search/movies/' + api_key + '?query='
        if len(kwargs) > 0:
            for key, val in kwargs.items():
                setattr(self, key, val)
        else:
            self.search()

    def search(self):
        """Search for this :class:`Person` via the Trakt.tv API"""
        def formatted(name):
            return name.replace(' ', '+').lower()
        ext = '/search/people.json/{}?query={}'.format(api_key,
                                                       formatted(self.name))
        url = self.base_url + ext
        response = requests.get(url)
        if response.status_code == 200:
            data = json.loads(response.content)
            if data is not None and data != []:
                for key, val in data.items():
                    setattr(self, key, val)
