"""A wrapper for the Trakt.tv REST API"""
import json
import logging
import requests
from hashlib import sha1
from collections import namedtuple
from .errors import *

version_info = (0, 1, 1)
__author__ = 'Jon Nappi'
__all__ = ['api_key', 'BaseAPI', 'server_time', 'authenticate', 'auth_post']
__version__ = '.'.join([str(i) for i in version_info])


@property
def api_key():
    """The current api key for accessing the Trakt.tv REST API system"""
    if '_TRAKT_APIKEY_' not in globals():
        globals()['_TRAKT_APIKEY_'] = None
    return globals()['_TRAKT_APIKEY_']
@api_key.setter
def api_key(value):
    globals()['_TRAKT_APIKEY_'] = value
@api_key.deleter
def api_key():
    globals()['_TRAKT_APIKEY_'] = None


@property
def server_time():
    """The current timestamp (PST) from the trakt server."""
    url = BaseAPI().base_url + '/server/time.json/{}'.format(api_key)
    response = requests.get(url)
    return response['timestamp']


def authenticate(username, password):
    """Provide authentication for a Trakt.tv account"""
    from .account import test
    if not test(username, password):
        raise InvalidCredentials
    globals()['_TRAKT_US_NAME_'] = username
    globals()['_TRAKT_PASS_WD_'] = sha1(password).hexdigest()


def auth_post(url, kwargs=None):
    """Create a post with provided authentication"""
    if '_TRAKT_US_NAME_' not in globals() or '_TRAKT_PASS_WD_' not in globals():
        raise InvalidCredentials
    user = globals()['_TRAKT_US_NAME_']
    password = globals()['_TRAKT_PASS_WD_']
    kwargs = kwargs or {}
    kwargs['username'] = user
    kwargs['password'] = password
    print url
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
