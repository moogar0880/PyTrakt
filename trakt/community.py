"""Interfaces to all of the TV objects offered by the Trakt.tv API"""
from . import api_key, BaseAPI
__author__ = 'Jon Nappi'
__all__ = ['Community', 'TraktRating', 'TraktStats']


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


class Community(BaseAPI):
    """Trakt.tv Community Report"""
    def __init__(self, search_type='all', start=None, end=None):
        super(Community, self).__init__()
        ext = 'community.json/{}/{}'.format(api_key, search_type)
        if start is not None and end is None:
            ext += '/' + str(start)
        elif start is None and end is not None:
            ext += '/' + str(end)
        else:
            ext += '/' + str(start) + '/' + str(end)
        data = self._get_(ext)
        for key, val in data.items():
            setattr(self, key, val)
