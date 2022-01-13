# -*- coding: utf-8 -*-
"""Objects, properties, and methods to be shared across other modules in the
trakt package
"""
import os
from collections import namedtuple
from functools import lru_cache

import requests

from trakt import decorators

__author__ = 'Jon Nappi'
__all__ = ['Airs', 'Alias', 'Comment', 'Genre',
           'init', 'BASE_URL', 'CLIENT_ID', 'CLIENT_SECRET', 'DEVICE_AUTH',
           'CONFIG_PATH', 'OAUTH_TOKEN',
           'OAUTH_REFRESH', 'PIN_AUTH', 'OAUTH_AUTH', 'AUTH_METHOD', 'api', 'config',
           'APPLICATION_ID']

#: The base url for the Trakt API. Can be modified to run against different
#: Trakt.tv environments
BASE_URL = 'https://api-v2launch.trakt.tv/'

#: The Trakt.tv OAuth Client ID for your OAuth Application
CLIENT_ID = None

#: The Trakt.tv OAuth Client Secret for your OAuth Application
CLIENT_SECRET = None

#: Default path for where to store your trakt.tv API authentication information
CONFIG_PATH = os.path.join(os.path.expanduser('~'), '.pytrakt.json')

#: Your personal Trakt.tv OAUTH Bearer Token
OAUTH_TOKEN = api_key = None

# Your OAUTH token expiration date
OAUTH_EXPIRES_AT = None

# Your OAUTH refresh token
OAUTH_REFRESH = None

#: Flag used to enable Trakt PIN authentication
PIN_AUTH = 'PIN'

#: Flag used to enable Trakt OAuth authentication
OAUTH_AUTH = 'OAUTH'

#: Flag used to enable Trakt OAuth device authentication
DEVICE_AUTH = 'DEVICE'

#: The currently enabled authentication method. Default is ``PIN_AUTH``
AUTH_METHOD = PIN_AUTH

#: The ID of the application to register with, when using PIN authentication
APPLICATION_ID = None

#: Global session to make requests with
session = requests.Session()


def init(*args, **kwargs):
    """Run the auth function specified by *AUTH_METHOD*"""
    from trakt.auth import init_auth

    return init_auth(AUTH_METHOD, *args, **kwargs)


Airs = namedtuple('Airs', ['day', 'time', 'timezone'])
Alias = namedtuple('Alias', ['title', 'country'])
Genre = namedtuple('Genre', ['name', 'slug'])
Comment = namedtuple('Comment', ['id', 'parent_id', 'created_at', 'comment',
                                 'spoiler', 'review', 'replies', 'user',
                                 'updated_at', 'likes', 'user_rating'])


@lru_cache(maxsize=None)
def config():
    from trakt.config import AuthConfig

    return AuthConfig(CONFIG_PATH).update(
        CLIENT_ID=CLIENT_ID,
        CLIENT_SECRET=CLIENT_SECRET,
        OAUTH_EXPIRES_AT=OAUTH_EXPIRES_AT,
        OAUTH_REFRESH=OAUTH_REFRESH,
        OAUTH_TOKEN=OAUTH_TOKEN,
    )


@lru_cache(maxsize=None)
def api():
    from trakt.api import HttpClient, TokenAuth

    client = HttpClient(BASE_URL, session)
    auth = TokenAuth(client=client, config=config())
    client.set_auth(auth)

    return client


# Backward compat with 3.x
delete = decorators.delete
get = decorators.get
post = decorators.post
put = decorators.put
