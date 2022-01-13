# -*- coding: utf-8 -*-
"""Interfaces to all of the People objects offered by the Trakt.tv API"""
import json
import logging
import os
from datetime import datetime, timezone, timedelta
from functools import lru_cache, wraps
from typing import NamedTuple, List, Optional
from urllib.parse import urljoin

from trakt import errors
from requests import Session

__author__ = 'Jon Nappi, Elan Ruusamäe'

from trakt.errors import OAuthException


class TraktApiParameters(NamedTuple):
    BASE_URL: str
    CLIENT_ID: Optional[str]
    CLIENT_SECRET: Optional[str]
    OAUTH_EXPIRES_AT: Optional[int]
    OAUTH_REFRESH: Optional[int]
    OAUTH_TOKEN: Optional[str]
    OAUTH_TOKEN_VALID: Optional[bool]
    REDIRECT_URI: str
    HEADERS: Optional[dict[str, str]]


class HttpClient:
    """Class for abstracting HTTP requests
    """

    def __init__(self, base_url: str, session: Session):
        self.base_url = base_url
        self.session = session
        self.logger = logging.getLogger('trakt.http_client')
        self.headers = {}

    def get(self, url: str):
        return self.request('get', url)

    def delete(self, url: str):
        self.request('delete', self.base_url + url)

    def post(self, url: str, data):
        return self.request('post', url, data=data)

    def put(self, url: str, data):
        return self.request('put', url, data=data)

    def set_headers(self, headers):
        self.headers.update(headers)

    def request(self, method, url, data=None):
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

        self.logger.debug('%s: %s', method, url)
        self.logger.debug('method, url :: %s, %s', method, url)
        if method == 'get':  # GETs need to pass data as params, not body
            response = self.session.request(method, url, headers=self.headers, params=data)
        else:
            response = self.session.request(method, url, headers=self.headers, data=json.dumps(data))
        self.logger.debug('RESPONSE [%s] (%s): %s', method, url, str(response))
        if response.status_code == 204:  # HTTP no content
            return None
        self.raise_if_needed(response)
        json_data = json.loads(response.content.decode('UTF-8', 'ignore'))
        return json_data

    def raise_if_needed(self, response):
        if response.status_code in self.error_map:
            raise self.error_map[response.status_code](response)

    @property
    @lru_cache(maxsize=1)
    def error_map(self):
        """Map HTTP response codes to exception types
        """

        # Get all of our exceptions except the base exception
        errs = [getattr(errors, att) for att in errors.__all__
                if att != 'TraktException']

        return {err.http_code: err for err in errs}


class TraktApiTokenAuth(dict):
    """Class dealing with loading and updating oauth refresh token.
    """

    def __init__(self, client: HttpClient, params: TraktApiParameters):
        super().__init__()
        self.client = client
        self.CONFIG_PATH = None
        self.update(**params._asdict())
        self.logger = logging.getLogger('trakt.api.oauth')

    def get_token(self):
        """Return client_id, client_token pair needed for Trakt.tv authentication
        """

        self.load_config()
        # Check token validity and refresh token if needed
        if (not self['OAUTH_TOKEN_VALID'] and self['OAUTH_EXPIRES_AT'] is not None
                and self['OAUTH_REFRESH'] is not None):
            self.validate_token()
        # For backwards compatibility with trakt<=2.3.0
        # if api_key is not None and OAUTH_TOKEN is None:
        #     OAUTH_TOKEN = api_key

        return [
            self['CLIENT_ID'],
            self['OAUTH_TOKEN'],
        ]

    def validate_token(self):
        """Check if current OAuth token has not expired"""

        current = datetime.now(tz=timezone.utc)
        expires_at = datetime.fromtimestamp(self['OAUTH_EXPIRES_AT'], tz=timezone.utc)
        if expires_at - current > timedelta(days=2):
            self['OAUTH_TOKEN_VALID'] = True
        else:
            self.refresh_token()

    def refresh_token(self):
        """Request Trakt API for a new valid OAuth token using refresh_token"""

        self.logger.info("OAuth token has expired, refreshing now...")
        url = urljoin(self['BASE_URL'], '/oauth/token')
        data = {
            'client_id': self['CLIENT_ID'],
            'client_secret': self['CLIENT_SECRET'],
            'refresh_token': self['OAUTH_REFRESH'],
            'redirect_uri': self['REDIRECT_URI'],
            'grant_type': 'refresh_token'
        }

        try:
            response = self.client.post(url, data)
        except OAuthException:
            self.logger.debug(
                "Rejected - Unable to refresh expired OAuth token, "
                "refresh_token is invalid"
            )
            return

        self['OAUTH_TOKEN'] = response.get("access_token")
        self['OAUTH_REFRESH'] = response.get("refresh_token")
        self['OAUTH_EXPIRES_AT'] = response.get("created_at") + response.get("expires_in")
        self['OAUTH_TOKEN_VALID'] = True

        self.logger.info(
            "OAuth token successfully refreshed, valid until {}".format(
                datetime.fromtimestamp(self['OAUTH_EXPIRES_AT'], tz=timezone.utc)
            )
        )
        self.store_token(
            CLIENT_ID=self['CLIENT_ID'], CLIENT_SECRET=self['CLIENT_SECRET'],
            OAUTH_TOKEN=self['OAUTH_TOKEN'], OAUTH_REFRESH=self['OAUTH_REFRESH'],
            OAUTH_EXPIRES_AT=self['OAUTH_EXPIRES_AT'],
        )

    def store_token(self, **kwargs):
        """Helper function used to store Trakt configurations at ``CONFIG_PATH``

        :param kwargs: Keyword args to store at ``CONFIG_PATH``
        """
        with open(self.CONFIG_PATH, 'w') as config_file:
            json.dump(kwargs, config_file)

    def load_config(self):
        """Manually load config from json config file."""
        # global CLIENT_ID, CLIENT_SECRET, OAUTH_TOKEN, OAUTH_EXPIRES_AT
        # global OAUTH_REFRESH, APPLICATION_ID, CONFIG_PATH
        if (self['CLIENT_ID'] is None or self['CLIENT_SECRET'] is None) and \
                os.path.exists(self.CONFIG_PATH):
            # Load in trakt API auth data from CONFIG_PATH
            with open(self.CONFIG_PATH) as config_file:
                config_data = json.load(config_file)

            if self['CLIENT_ID'] is None:
                self['CLIENT_ID'] = config_data.get('CLIENT_ID', None)
            if self['CLIENT_SECRET'] is None:
                self['CLIENT_SECRET'] = config_data.get('CLIENT_SECRET', None)
            if self['OAUTH_TOKEN'] is None:
                self['OAUTH_TOKEN'] = config_data.get('OAUTH_TOKEN', None)
            if self['OAUTH_EXPIRES_AT'] is None:
                self['OAUTH_EXPIRES_AT'] = config_data.get('OAUTH_EXPIRES_AT', None)
            if self['OAUTH_REFRESH'] is None:
                self['OAUTH_REFRESH'] = config_data.get('OAUTH_REFRESH', None)
            if self['APPLICATION_ID'] is None:
                self['APPLICATION_ID'] = config_data.get('APPLICATION_ID', None)


class TraktApi:
    """This class contains all of the functionality required for interfacing
    with the Trakt.tv API
    """

    def __init__(self, client: HttpClient, params: TraktApiParameters):
        self.client = client
        self.token_auth = TraktApiTokenAuth(client=self.client, params=params)
        self.logger = logging.getLogger('trakt.api')

    def get(self, url: str):
        self.authorize()
        return self.client.get(url)

    def delete(self, url: str):
        self.authorize()
        self.client.delete(url)

    def post(self, url: str, data):
        self.authorize()
        return self.client.post(url, data=data)

    def put(self, url: str, data):
        self.authorize()
        return self.client.put(url, data=data)

    @lru_cache(maxsize=None)
    def authorize(self):
        [client_id, client_token] = self.token_auth.get_token()

        headers = {
            'trakt-api-key': client_id,
            'Authorization': f'Bearer {client_token}',
        }
        self.logger.debug('headers: %s', str(headers))
        self.client.set_headers(headers)

        return headers
