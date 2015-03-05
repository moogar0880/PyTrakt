"""Objects, properties, and methods to be shared across other modules in the
trakt package

import logging
logging.basicConfig(level=logging.DEBUG)
import trakt
trakt.api_key = '3f15016ea3ef5bd3a03bbd90c5824a254f0d56626ee3b99a8c28290e2e05d3df'
from trakt.tv import TVShow
crowd = TVShow('The IT Crowd')
"""
from __future__ import print_function
import os
import json
import logging
import requests
from functools import wraps
from collections import namedtuple
from requests_oauthlib import OAuth2Session

from . import errors

__author__ = 'Jon Nappi'
__all__ = ['Airs', 'Alias', 'Comment', 'Genre', 'Translation', 'get', 'delete',
           'post', 'put', 'init', 'api_key']

#: The base url for the Trakt API. Can be modified to run against different
#: Trakt.tv environments
BASE_URL = 'https://api.trakt.tv/'

#: The Trakt.tv OAuth Client ID for your OAuth Application
CLIENT_ID = None

#: The Trakt.tv OAuth Client Secret for your OAuth Application
CLIENT_SECRET = None

#: The OAuth2 Redirect URI for your OAuth Application
REDIRECT_URI = 'urn:ietf:wg:oauth:2.0:oob'

#: Default request HEADERS
HEADERS = {'Content-Type': 'application/json', 'trakt-api-version': '2'}

#: Default path for where to store your trakt.tv API authentication information
CONFIG_PATH = os.path.join(os.path.expanduser('~'), '.pytrakt.json')

#: Your personal Trakt.tv API Key
api_key = None


def init(username, client_id=None, client_secret=None, store=False):
    """Generate an access_token to allow your application to authenticate via
    OAuth

    :param username: Your trakt.tv username
    :param client_id: Your Trakt OAuth Application's Client ID
    :param client_secret: Your Trakt OAuth Application's Client Secret
    :param store: Boolean flag used to determine if your trakt api auth data
        should be stored locally on the system. Default is :const:`False` for the
        security conscious
    :return: Your OAuth access token
    """
    global CLIENT_ID, CLIENT_SECRET, api_key
    if client_id is None and client_secret is None:
        print('If you do not have a client ID and secret. Please visit the '
              'following url to create them.')
        print('http://trakt.tv/oauth/applications')
        client_id = input('Please enter your client id: ')
        client_secret = input('Please enter your client secret: ')
    CLIENT_ID, client_secret = client_id, client_secret
    HEADERS['trakt-api-key'] = CLIENT_ID

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
    api_key = oauth.token['access_token']

    if store:
        data = {'CLIENT_ID': CLIENT_ID, 'CLIENT_SECRET': CLIENT_SECRET,
                'api_key': api_key}
        with open(CONFIG_PATH, 'w') as config_file:
            json.dump(data, config_file)

    return oauth.token['access_token']


Airs = namedtuple('Airs', ['day', 'time', 'timezone'])
Alias = namedtuple('Alias', ['title', 'country'])
Genre = namedtuple('Genre', ['name', 'slug'])
Comment = namedtuple('Comment', ['id', 'parent_id', 'created_at', 'comment',
                                 'spoiler', 'review', 'replies', 'user',
                                 'likes'])
Translation = namedtuple('Translation', ['title', 'overview', 'tagline',
                                         'language'])


def _bootstrapped(f):
    """Bootstrap your authentication environment when authentication is needed
    and if a file at `CONFIG_PATH` exists. The process is completed by setting
    the client id header.
    """
    @wraps(f)
    def inner(*args, **kwargs):
        global CLIENT_ID, CLIENT_SECRET, api_key
        if CLIENT_ID is None or CLIENT_SECRET is None and \
                os.path.exists(CONFIG_PATH):
            # Load in trakt API auth data fron CONFIG_PATH
            with open(CONFIG_PATH) as config_file:
                config_data = json.load(config_file)

            CLIENT_ID = config_data['CLIENT_ID']
            CLIENT_SECRET = config_data['CLIENT_SECRET']
            api_key = config_data['api_key']

            HEADERS['trakt-api-key'] = CLIENT_ID
        return f(*args, **kwargs)
    return inner


class Core(object):
    """This class contains all of the functionality required for interfacing
    with the Trakt.tv API
    """

    def __init__(self):
        """Create a :class:`Core` instance and give it a logger attribute"""
        self.logger = logging.getLogger('trakt.core')

        # Get all of our exceptions except the base exception
        errs = [getattr(errors, att) for att in errors.__all__
                if att != 'TraktException']

        # Map HTTP response codes to exception types
        self.error_map = {err.http_code: err for err in errs}

    @staticmethod
    def _get_first(f, *args, **kwargs):
        """Extract the first value from the provided generator function *f*

        :param f: A generator function to extract data from
        :param args: Non keyword args for the generator function
        :param kwargs: Keyword args for the generator function
        :return: The full url for the resource, a generator, and either a data
            payload or `None`
        """
        generator = f(*args, **kwargs)
        uri = next(generator)
        if not isinstance(uri, (str, tuple)):
            # Allow properties to safetly yield arbitrary data
            return uri
        if isinstance(uri, tuple):
            uri, data = uri
            return BASE_URL + uri, generator, data
        else:
            return BASE_URL + uri, generator, None

    def _handle_request(self, method, url, data=None):
        """Handle actually talking out to the trakt API, logging out debug
        information, raising any relevant `TraktException` Exception types,
        and extracting and returning JSON data

        :param method: The HTTP method we're executing on. Will be one of
            post, put, delete, get
        :param url: The fully qualified url to send our request to
        :param data: Optional data payload to send to the API
        :return: The decoded JSON response from the Trakt API
        :raises TraktException: If any non-200 return code is encountered
        """
        self.logger.debug('GET: %s', url)
        HEADERS['Authorization'] = 'Bearer {}'.format(api_key)
        response = requests.request(method, url, params=data, headers=HEADERS)
        self.logger.debug('RESPONSE [GET] (%s): %s', url, str(response))
        if response.status_code in self.error_map:
            raise self.error_map[response.status_code]()
        json_data = json.loads(response.content.decode('UTF-8', 'ignore'))
        return json_data

    @_bootstrapped
    def get(self, f):
        """Perform a HTTP GET request using the provided uri yielded from the
        *f* co-routine. The processed JSON results are then sent back to the
        co-routine for post-processing, the results of which are then returned

        :param f: Generator co-routine that yields uri, args, and processed
            results
        :return: The results of the generator co-routine
        """
        @wraps(f)
        def inner(*args, **kwargs):
            url, generator, _ = self._get_first(f, *args, **kwargs)
            json_data = self._handle_request('get', url)
            try:
                return generator.send(json_data)
            except StopIteration:
                return None
        return inner

    @_bootstrapped
    def delete(self, f):
        """Perform an HTTP DELETE request using the provided uri

        :param f: Function that returns a uri to delete to
        """
        @wraps(f)
        def inner(*args, **kwargs):
            uri = f(*args, **kwargs)
            url = BASE_URL + uri
            self._handle_request('delete', url)
        return inner

    @_bootstrapped
    def post(self, f):
        """Perform an HTTP POST request using the provided uri and optional
        args yielded from the *f* co-routine. The processed JSON results are
        then sent back to the co-routine for post-processing, the results of
        which are then returned

        :param f: Generator co-routine that yields uri, args, and processed
            results
        :return: The results of the generator co-routine
        """
        @wraps(f)
        def inner(*args, **kwargs):
            url, generator, args = self._get_first(f, *args, **kwargs)
            json_data = self._handle_request('post', url, data=args)
            try:
                return generator.send(json_data)
            except StopIteration:
                return None
        return inner

    @_bootstrapped
    def put(self, f):
        """Perform an HTTP PUT request using the provided uri and optional args
        yielded from the *f* co-routine. The processed JSON results are then
        sent back to the co-routine for post-processing, the results of which
        are then returned

        :param f: Generator co-routine that yields uri, args, and processed
            results
        :return: The results of the generator co-routine
        """
        @wraps(f)
        def inner(*args, **kwargs):
            url, generator, args = self._get_first(f, *args, **kwargs)
            json_data = self._handle_request('put', url, data=args)
            try:
                return generator.send(json_data)
            except StopIteration:
                return None
        return inner

# Here we can simplify the code in each module by exporting these instance
# method decorators as if they were simple functions.
CORE = Core()
get = CORE.get
post = CORE.post
delete = CORE.delete
put = CORE.put
