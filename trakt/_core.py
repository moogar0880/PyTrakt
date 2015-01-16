"""Objects, properties, and methods to be shared across other modules in the
trakt package
"""
import re
import json
import logging
import requests
import unicodedata
from hashlib import sha1
from collections import namedtuple

from proxy_tools import module_property

import trakt
from .errors import *

__author__ = 'Jon Nappi'
__all__ = ['BaseAPI', 'server_time', 'authenticate', 'auth_post', 'Genre',
           'Comment', 'slugify']


@module_property
def server_time():
    """Get the current timestamp (PST) from the trakt server."""
    url = BaseAPI.base_url + 'server/time.json/{}'.format(trakt.api_key)
    response = requests.get(url)
    data = json.loads(response.content.decode('UTF-8'))
    return data.get('timestamp')


def authenticate(username, password):
    """Provide authentication for a Trakt.tv account"""
    from . import account
    if not account.test(username, password):
        raise InvalidCredentials
    globals()['_TRAKT_US_NAME_'] = username
    globals()['_TRAKT_PASS_WD_'] = sha1(password.encode('UTF-8')).hexdigest()


def auth_post(url, kwargs=None):
    """Create a post with provided authentication"""
    if '_TRAKT_US_NAME_' not in globals() or '_TRAKT_PASS_WD_' not in globals():
        raise InvalidCredentials
    kwargs = kwargs or {}
    kwargs['username'] = globals()['_TRAKT_US_NAME_']
    kwargs['password'] = globals()['_TRAKT_PASS_WD_']
    response = requests.post(url, json.dumps(kwargs))
    return response


Genre = namedtuple('Genre', ['name', 'slug'])
Comment = namedtuple('Comment', ['id', 'inserted', 'text', 'text_html',
                                 'spoiler', 'type', 'likes', 'replies', 'user',
                                 'user_ratings'])


def slugify(value):
    """Converts to lowercase, removes non-word characters (alphanumerics and
    underscores) and converts spaces to hyphens. Also strips leading and
    trailing whitespace.

    Borrowed from django.utils.text.slugify with some slight modifications
    """
    value = unicodedata.normalize('NFKD',
                                  value).encode('ascii',
                                                'ignore').decode('ascii')
    value = re.sub('[^\w\s-]', '', value).strip().lower()
    return re.sub('[-\s]+', '-', value)


class BaseAPI(object):
    """Base class containing all basic functionality of a Trakt.tv API call"""
    base_url = 'https://api.trakt.tv/'
    _logger = logging.getLogger('Trakt.API')

    @classmethod
    def _get_(cls, uri, args=None):
        """Perform a GET API call against the Trakt.tv API against *uri*

        :param uri: The uri extension to GET from
        """
        url = cls.base_url + uri
        cls._logger.debug('GET: {}'.format(url))
        response = requests.get(url, params=args)
        data = json.loads(response.content.decode('UTF-8', 'ignore'))
        return data

    @classmethod
    def _post_(cls, uri, args=None):
        """Perform a POST API call against the Trakt.tv API against *uri*,
        passing args

        :param uri: The uri extension to POST to
        :param args: The args to pass to Trakt.tv
        """
        url = cls.base_url + uri
        cls._logger.debug('POST: {}: <{}>'.format(url, args))
        response = auth_post(url, args)
        data = json.loads(response.content.decode('UTF-8', 'ignore'))
        return data
