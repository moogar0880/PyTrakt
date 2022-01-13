# -*- coding: utf-8 -*-
"""Interfaces to all of the People objects offered by the Trakt.tv API"""
import json
import logging
import os
from datetime import datetime, timezone, timedelta
from functools import lru_cache, wraps
from typing import NamedTuple, List, Optional
from urllib.parse import urljoin
from requests.auth import AuthBase

from trakt import errors
from requests import Session

__author__ = 'Jon Nappi, Elan Ruusamäe'

from trakt.config import AuthConfig
from trakt.errors import OAuthException


class HttpClient:
    """Class for abstracting HTTP requests
    """

    #: Default request HEADERS
    headers = {'Content-Type': 'application/json', 'trakt-api-version': '2'}

    def __init__(self, base_url: str, session: Session):
        self.base_url = base_url
        self.session = session
        self.logger = logging.getLogger('trakt.http_client')
        self.auth = None

    def get(self, url: str):
        return self.request('get', url)

    def delete(self, url: str):
        self.request('delete', url)

    def post(self, url: str, data):
        return self.request('post', url, data=data)

    def put(self, url: str, data):
        return self.request('put', url, data=data)

    def set_auth(self, auth):
        self.auth = auth

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

        url = self.base_url + url
        self.logger.debug('%s: %s', method, url)
        self.logger.debug('method, url :: %s, %s', method, url)
        if method == 'get':  # GETs need to pass data as params, not body
            response = self.session.request(method, url, headers=self.headers, auth=self.auth, params=data)
        else:
            response = self.session.request(method, url, headers=self.headers, auth=self.auth, data=json.dumps(data))
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
    @lru_cache(maxsize=None)
    def error_map(self):
        """Map HTTP response codes to exception types
        """

        # Get all of our exceptions except the base exception
        errs = [getattr(errors, att) for att in errors.__all__
                if att != 'TraktException']

        return {err.http_code: err for err in errs}


class TokenAuth(AuthBase):
    """Attaches Trakt.tv token Authentication to the given Request object."""

    # OAuth token validity checked
    OAUTH_TOKEN_VALID = None

    def __init__(self, client: HttpClient, config: AuthConfig):
        super().__init__()
        self.config = config
        self.client = client
        self.logger = logging.getLogger('trakt.api.oauth')

    def __call__(self, r):
        [client_id, client_token] = self.get_token()

        r.headers.update({
            'trakt-api-key': client_id,
            'Authorization': f'Bearer {client_token}',
        })
        return r

    def get_token(self):
        """Return client_id, client_token pair needed for Trakt.tv authentication
        """

        self.load_config()
        # Check token validity and refresh token if needed
        if not self.OAUTH_TOKEN_VALID and self.config.OAUTH_EXPIRES_AT is not None and self.config.OAUTH_REFRESH is not None:
            self.validate_token()

        return [
            self.config.CLIENT_ID,
            self.config.OAUTH_TOKEN,
        ]

    def validate_token(self):
        """Check if current OAuth token has not expired"""

        current = datetime.now(tz=timezone.utc)
        expires_at = datetime.fromtimestamp(self.config.OAUTH_EXPIRES_AT, tz=timezone.utc)
        if expires_at - current > timedelta(days=2):
            self.OAUTH_TOKEN_VALID = True
        else:
            self.refresh_token()

    def refresh_token(self):
        """Request Trakt API for a new valid OAuth token using refresh_token"""

        self.logger.info("OAuth token has expired, refreshing now...")
        data = {
            'client_id': self.config.CLIENT_ID,
            'client_secret': self.config.CLIENT_SECRET,
            'refresh_token': self.config.OAUTH_REFRESH,
            'redirect_uri': self.config.REDIRECT_URI,
            'grant_type': 'refresh_token'
        }

        try:
            response = self.client.post('/oauth/token', data)
        except OAuthException:
            self.logger.debug(
                "Rejected - Unable to refresh expired OAuth token, "
                "refresh_token is invalid"
            )
            return

        self.config.OAUTH_TOKEN = response.get("access_token")
        self.config.OAUTH_REFRESH = response.get("refresh_token")
        self.config.OAUTH_EXPIRES_AT = response.get("created_at") + response.get("expires_in")
        self.OAUTH_TOKEN_VALID = True

        self.logger.info(
            "OAuth token successfully refreshed, valid until {}".format(
                datetime.fromtimestamp(self.config.OAUTH_EXPIRES_AT, tz=timezone.utc)
            )
        )
        self.config.store(
            CLIENT_ID=self.config.CLIENT_ID,
            CLIENT_SECRET=self.config.CLIENT_SECRET,
            OAUTH_TOKEN=self.config.OAUTH_TOKEN,
            OAUTH_REFRESH=self.config.OAUTH_REFRESH,
            OAUTH_EXPIRES_AT=self.config.OAUTH_EXPIRES_AT,
        )

    def load_config(self):
        """Manually load config from json config file."""

        if self.config.CLIENT_ID is not None and self.config.CLIENT_SECRET is not None or not self.config.exists():
            return

        config_data = self.config.load()

        keys = [
            'APPLICATION_ID',
            'CLIENT_ID',
            'CLIENT_SECRET',
            'OAUTH_EXPIRES_AT',
            'OAUTH_REFRESH',
            'OAUTH_TOKEN',
        ]

        for key in keys:
            if self.config.get(key) is not None:
                continue

            self.config.set(key, config_data.get(key, None))
