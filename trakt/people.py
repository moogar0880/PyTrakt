"""Interfaces to all of the People objects offered by the Trakt.tv API"""
import json
import requests

from . import BaseAPI
import trakt
__author__ = 'Jon Nappi'
__all__ = ['Person']


class Person(BaseAPI):
    """A Class representing a Movie object"""
    def __init__(self, name, **kwargs):
        super(Person, self).__init__()
        self.name = name
        self.url = self.biography = self.birthplace = self.tmdb_id = None
        self.birthday = None
        self.images = []
        self.url_extension = 'search/movies/{}?query='.format(trakt.api_key)
        if len(kwargs) > 0:
            for key, val in kwargs.items():
                setattr(self, key, val)
        else:
            self.search()

    def search(self):
        """Search for this :class:`Person` via the Trakt.tv API"""
        def formatted(name):
            return name.replace(' ', '+').lower()

        ext = 'search/people.json/{}?query={}'.format(trakt.api_key,
                                                      formatted(self.name))
        url = self.base_url + ext
        response = requests.get(url)
        if response.status_code == 200:
            data = json.loads(response.content.decode('UTF-8'))
            for person in data:
                if person['name'] == self.name:
                    for key, val in person.items():
                        setattr(self, key, val)
                    break

    def __str__(self):
        """String representation of a :class:`Person`"""
        return '<Person>: {}'.format(self.name)
    __repr__ = __str__
