"""Objects, properties, and methods to be shared across other modules in the
trakt package
"""
import re
import json
import logging
import requests
import unicodedata
from collections import namedtuple
from requests_oauthlib import OAuth2Session

from proxy_tools import module_property

import trakt

__author__ = 'Jon Nappi'
__all__ = ['BaseAPI', 'server_time', 'Genre', 'Comment', 'slugify', 'HEADERS']

CLIENT_ID = 'd0113f50a0c6ff4d8977427a81e34057ecd54ebfa245f481d1e45baa47129629'
CLIENT_SECRET = '807a4162cb179d4ba95e8a8cb23c7afd4386b66ef3f9a71de692b4c94b01e1ac'
REDIRECT_URI = 'urn:ietf:wg:oauth:2.0:oob'

HEADERS = {'Content-Type': 'application/json',
           'trakt-api-version': '2',
           'trakt-api-key': CLIENT_ID}


def init(username):
    """Generate an access_token to allow the the PyTrakt application to
    authenticate via OAuth

    :param username: Your trakt.tv username
    :return: Your OAuth access token
    """
    authorization_base_url = 'https://api.trakt.tv/oauth/authorize'
    token_url = 'https://api.trakt.tv/oauth/token'

    # OAuth endpoints given in the API documentation
    oauth = OAuth2Session(CLIENT_ID, redirect_uri=REDIRECT_URI, state=None)

    # Redirect user to Trakt for authorization
    authorization_url, state = oauth.authorization_url(authorization_base_url,
                                                       username=username)
    print('Please go here and authorize,', authorization_url)

    # Get the authorization verifier code from the callback url
    response = input('Paste the Code returned here: ')

    # Fetch, assign, and return the access token
    oauth.fetch_token(token_url, client_secret=CLIENT_SECRET, code=response)
    trakt.api_key = oauth.token['access_token']
    return oauth.token['access_token']


@module_property
def server_time():
    """Get the current timestamp (PST) from the trakt server."""
    uri = 'server/time.json/{}'.format(trakt.api_key)
    return BaseAPI._get_(uri).get('timestamp', None)


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
        HEADERS['Authorization'] = 'Bearer {}'.format(trakt.api_key)
        cls._logger.debug('HEAD: {}'.format(HEADERS))
        response = requests.get(url, params=args, headers=HEADERS)
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
        cls._logger.debug('POST: {}: [{}] <{}>'.format(url, HEADERS, args))
        HEADERS['Authorization'] = 'Bearer {}'.format(trakt.api_key)
        response = requests.post(url, json.dumps(args), headers=HEADERS)
        data = json.loads(response.content.decode('UTF-8', 'ignore'))
        return data
