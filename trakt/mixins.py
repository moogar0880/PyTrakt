# -*- coding: utf-8 -*-
"""Contains various MixIns"""

__author__ = 'Jon Nappi, Elan Ruusamäe'


class IdsMixin:
    """
    Provides Mixin to translate "ids" array
    to appropriate provider ids in base class.

    This is replacement for extract_ids() utility method.
    """

    def __init__(self):
        self._ids = {
            'tmdb': None,
            'trakt': None,
            'tvdb': None,
            'slug': None,
            'tvrage': None,
        }
        self.slug = None

    @property
    def ids(self):
        """
        Accessor to the trakt, imdb, and tmdb ids,
        as well as the trakt.tv slug
        """
        return {
            'ids': {
                'imdb': self.imdb,
                'slug': self.slug,
                'tmdb': self.tmdb,
                'trakt': self.trakt,
            }
        }

    @property
    def imdb(self):
        return self._ids.get('imdb', None)

    @property
    def tmdb(self):
        return self._ids.get('tmdb', None)

    @property
    def trakt(self):
        return self._ids.get('trakt', None)

    @property
    def tvdb(self):
        return self._ids.get('tvdb', None)

    @property
    def tvrage(self):
        return self._ids.get('tvrage', None)
