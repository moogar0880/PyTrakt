# -*- coding: utf-8 -*-
"""Interfaces to all of the People objects offered by the Trakt.tv API"""
from trakt.core import get
from trakt.utils import slugify, extract_ids

__author__ = 'Jon Nappi'
__all__ = ['Person']


class Person(object):
    """A Class representing a trakt.tv Person such as an Actor or Director"""
    def __init__(self, name, slug=None, **kwargs):
        super(Person, self).__init__()
        self.name = name
        self.biography = self.birthplace = self.tmdb_id = self.birthday = None
        self.job = self.character = self._images = None
        self.slug = slug or slugify(self.name)

        if len(kwargs) > 0:
            self._build(kwargs)
        else:
            self._get()

    @property
    def ext(self):
        return 'people/{id}'.format(id=self.slug)

    @property
    def ext_full(self):
        return self.ext + '?extended=full'

    @property
    def images_ext(self):
        return self.ext + '?extended=images'

    @get
    def _get(self):
        data = yield self.ext_full
        self._build(data)

    def _build(self, data):
        extract_ids(data)
        for key, val in data.items():
            try:
                setattr(self, key, val)
            except AttributeError as ae:
                if not hasattr(self, '_' + key):
                    raise ae

    @property
    @get
    def images(self):
        """All of the artwork associated with this :class:`Person`"""
        if self._images is None:
            data = yield self.images_ext
            self._images = data.get('images', {})
        yield self._images

    def __str__(self):
        """String representation of a :class:`Person`"""
        return '<Person>: {0}'.format(self.name)
    __repr__ = __str__
