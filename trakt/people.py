"""Interfaces to all of the People objects offered by the Trakt.tv API"""
from . import BaseAPI
import trakt

__author__ = 'Jon Nappi'
__all__ = ['Person']


class Person(BaseAPI):
    """A Class representing a trakt.tv Person such as an Actor or Director"""
    def __init__(self, name, **kwargs):
        super(Person, self).__init__()
        self.name = name
        self.url = self.biography = self.birthplace = self.tmdb_id = None
        self.birthday = self.job = self.character = None
        self.images = []
        if len(kwargs) > 0:
            for key, val in kwargs.items():
                setattr(self, key, val)
        else:
            self._search()

    def _search(self):
        """Search for this :class:`Person` via the Trakt.tv API"""
        def formatted(name):
            """Because actors aren't likely to have special characters in their
            name (although they're probably more likely to than anyone else), we
            don't need to slugify their names, just replace spaces and lower()
            """
            return name.replace(' ', '+').lower()

        ext = 'search/people.json/{}?query={}'.format(trakt.api_key,
                                                      formatted(self.name))
        data = self._get_(ext)
        for person in data:
            if person['name'] == self.name:
                for key, val in person.items():
                    setattr(self, key, val)
                break

    def __str__(self):
        """String representation of a :class:`Person`"""
        return '<Person>: {}'.format(self.name)
    __repr__ = __str__
