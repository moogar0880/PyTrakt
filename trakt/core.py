# -*- coding: utf-8 -*-
"""Objects, properties, and methods to be shared across other modules in the
trakt package
"""
import os
from dataclasses import dataclass
from typing import Optional

import requests
from collections import namedtuple
from functools import lru_cache

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


@dataclass
class AuthConfig:
    CLIENT_ID: Optional[str]
    CLIENT_SECRET: Optional[str]
    OAUTH_EXPIRES_AT: Optional[int]
    OAUTH_REFRESH: Optional[int]
    OAUTH_TOKEN: Optional[str]
    #: The OAuth2 Redirect URI for your OAuth Application
    REDIRECT_URI: str = 'urn:ietf:wg:oauth:2.0:oob'

    def update(self, **kwargs):
        for name, value in kwargs.items():
            self.__setattr__(name, value)

        return self


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
    from trakt.config import Config

    return Config(CONFIG_PATH)


@lru_cache(maxsize=None)
def api():
    from trakt.api import HttpClient
    from trakt.api import TokenAuth

    global OAUTH_EXPIRES_AT
    global OAUTH_REFRESH, OAUTH_TOKEN
    global CLIENT_ID, CLIENT_SECRET

    params = dict(
        CLIENT_ID=CLIENT_ID,
        CLIENT_SECRET=CLIENT_SECRET,
        OAUTH_EXPIRES_AT=OAUTH_EXPIRES_AT,
        OAUTH_REFRESH=OAUTH_REFRESH,
        OAUTH_TOKEN=OAUTH_TOKEN,
    )
    client = HttpClient(BASE_URL, session)
    c = config().update(**params)
    auth = TokenAuth(client=client, config=c)
    client.set_auth(auth)

    return client
