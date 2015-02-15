"""Objects, properties, and methods to be shared across other modules in the
trakt package
"""
import json
import logging
import requests
from functools import wraps
from collections import namedtuple
from requests_oauthlib import OAuth2Session

import trakt

__author__ = 'Jon Nappi'
__all__ = ['Airs', 'Alias', 'Comment', 'Genre', 'Translation', 'get', 'delete',
           'post', 'put', 'init']

BASE_URL = 'https://api.trakt.tv/'
CLIENT_ID = 'd0113f50a0c6ff4d8977427a81e34057ecd54ebfa245f481d1e45baa47129629'
CLIENT_SECRET = ('807a4162cb179d4ba95e8a8cb23c7afd4386b66ef3f9a71de692b4c94b01'
                 'e1ac')
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


Airs = namedtuple('Airs', ['day', 'time', 'timezone'])
Alias = namedtuple('Alias', ['title', 'country'])
Genre = namedtuple('Genre', ['name', 'slug'])
Comment = namedtuple('Comment', ['id', 'parent_id', 'created_at', 'comment',
                                 'spoiler', 'review', 'replies', 'user',
                                 'likes'])
Translation = namedtuple('Translation', ['title', 'overview', 'tagline',
                                         'language'])


def get(f):
    """Perform a HTTP GET request using the provided uri yielded from the *f*
    co-routine. The processed JSON results are then sent back to the co-routine
    for post-processing, the results of which are then returned

    :param f: Generator co-routine that yields uri, args, and processed results
    :return: The results of the generator co-routine
    """
    @wraps(f)
    def inner(*args, **kwargs):
        generator = f(*args, **kwargs)
        uri = next(generator)
        if not isinstance(uri, (str, tuple)):
            # Allow properties to safetly yield arbitrary data
            return uri
        url = BASE_URL + uri
        logging.debug('GET: %s', url)
        HEADERS['Authorization'] = 'Bearer {}'.format(trakt.api_key)
        response = requests.get(url, headers=HEADERS)
        json_data = json.loads(response.content.decode('UTF-8', 'ignore'))
        try:
            return generator.send(json_data)
        except StopIteration:
            return None
    return inner


def delete(f):
    """Perform an HTTP DELETE request using the provided uri

    :param f: Function that returns a uri to delete to
    """
    @wraps(f)
    def inner(*args, **kwargs):
        uri = f(*args, **kwargs)
        url = BASE_URL + uri
        logging.debug('DELETE: %s', url)
        HEADERS['Authorization'] = 'Bearer {}'.format(trakt.api_key)
        requests.delete(url, headers=HEADERS)
    return inner


def post(f):
    """Perform an HTTP POST request using the provided uri and optional args
    yielded from the *f* co-routine. The processed JSON results are then sent
    back to the co-routine for post-processing, the results of which are then
    returned

    :param f: Generator co-routine that yields uri, args, and processed results
    :return: The results of the generator co-routine
    """
    @wraps(f)
    def inner(*args, **kwargs):
        generator = f(*args, **kwargs)
        uri, data = next(generator)
        url = BASE_URL + uri
        logging.debug('POST: %s', url)
        HEADERS['Authorization'] = 'Bearer {}'.format(trakt.api_key)
        response = requests.post(url, params=data, headers=HEADERS)
        json_data = json.loads(response.content.decode('UTF-8', 'ignore'))
        try:
            return generator.send(json_data)
        except StopIteration:
            return None
    return inner


def put(f):
    """Perform an HTTP PUT request using the provided uri and optional args
    yielded from the *f* co-routine. The processed JSON results are then sent
    back to the co-routine for post-processing, the results of which are then
    returned

    :param f: Generator co-routine that yields uri, args, and processed results
    :return: The results of the generator co-routine
    """
    @wraps(f)
    def inner(*args, **kwargs):
        generator = f(*args, **kwargs)
        uri, data = next(generator)
        url = BASE_URL + uri
        logging.debug('PUT: %s', url)
        HEADERS['Authorization'] = 'Bearer {}'.format(trakt.api_key)
        response = requests.put(url, params=args, headers=HEADERS)
        json_data = json.loads(response.content.decode('UTF-8', 'ignore'))
        try:
            return generator.send(json_data)
        except StopIteration:
            return None
    return inner
