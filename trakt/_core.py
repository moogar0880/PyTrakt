"""Objects, properties, and methods to be shared across other modules in the
trakt package
"""
import json
import logging
from hashlib import sha1
from collections import namedtuple

from proxy_tools import module_property

import trakt
from .errors import *
__author__ = 'Jon Nappi'
__all__ = ['BaseAPI', 'server_time', 'authenticate', 'auth_post', 'Genre',
           'Comment']


@module_property
def server_time():
    """Get the current timestamp (PST) from the trakt server."""
    import requests
    url = BaseAPI().base_url + 'server/time.json/{}'.format(trakt.api_key)
    print(url)
    response = requests.get(url)
    data = json.loads(response.content.decode('UTF-8'))
    from pprint import pprint
    pprint(data)
    return data['timestamp']


def authenticate(username, password):
    """Provide authentication for a Trakt.tv account"""
    from .account import test
    if not test(username, password):
        raise InvalidCredentials
    globals()['_TRAKT_US_NAME_'] = username
    globals()['_TRAKT_PASS_WD_'] = sha1(password.encode('UTF-8')).hexdigest()


def auth_post(url, kwargs=None):
    """Create a post with provided authentication"""
    import requests
    if '_TRAKT_US_NAME_' not in globals() or '_TRAKT_PASS_WD_' not in globals():
        raise InvalidCredentials
    user = globals()['_TRAKT_US_NAME_']
    password = globals()['_TRAKT_PASS_WD_']
    kwargs = kwargs or {}
    kwargs['username'] = user
    kwargs['password'] = password
    response = requests.post(url, kwargs)
    return response


Genre = namedtuple('Genre', ['name', 'slug'])
Comment = namedtuple('Comment', ['id', 'inserted', 'text', 'text_html',
                                 'spoiler', 'type', 'likes', 'replies', 'user',
                                 'user_ratings'])


class BaseAPI(object):
    """Base class containing all basic functionality of a Trakt.tv API call"""
    def __init__(self):
        super(BaseAPI, self).__init__()
        self.base_url = 'http://api.trakt.tv/'
        self.logger = logging.getLogger('Trakt.API')

    def _get_(self, uri):
        """Perform a GET API call against the Trakt.tv API against *uri*

        :param uri: The uri extension to GET from
        """
        import requests
        url = self.base_url + uri
        self.logger.debug('GET: {}'.format(url))
        response = requests.get(url)
        data = json.loads(response.content.decode('UTF-8'))
        return data

    def _post_(self, uri, args=None):
        """Perform a POST API call against the Trakt.tv API against *uri*,
        passing args

        :param uri: The uri extension to POST to
        :param args: The args to pass to Trakt.tv
        """
        url = self.base_url + uri
        self.logger.debug('POST: {}: <{}>'.format(url, args))
        response = auth_post(url, args)
        data = json.loads(response.content.decode('UTF-8'))
        return data
