# -*- coding: utf-8 -*-
"""Class for config loading/storing"""

__author__ = 'Elan Ruusamäe'

import json
from dataclasses import dataclass
from os.path import exists
from typing import Optional


@dataclass
class AuthConfig:
    CLIENT_ID: Optional[str]
    CLIENT_SECRET: Optional[str]
    OAUTH_EXPIRES_AT: Optional[int]
    OAUTH_REFRESH: Optional[int]
    OAUTH_TOKEN: Optional[str]
    #: The OAuth2 Redirect URI for your OAuth Application
    REDIRECT_URI: str = 'urn:ietf:wg:oauth:2.0:oob'

    def __init__(self, config_path):
        self.config_path = config_path

    def have_refresh_token(self):
        # Check token validity and refresh token if needed
        return self.OAUTH_EXPIRES_AT is not None and self.OAUTH_REFRESH is not None

    def update(self, **kwargs):
        for name, value in kwargs.items():
            self.__setattr__(name, value)

        return self

    def get(self, name, default=None):
        try:
            return self.__getattribute__(name)
        except AttributeError:
            return default

    def set(self, name, value):
        self.__setattr__(name, value)

    def exists(self):
        return exists(self.config_path)

    def load(self):
        """
        Load in trakt API auth data from CONFIG_PATH
        """
        if not self.exists():
            return {}

        # Load in trakt API auth data from CONFIG_PATH
        with open(self.config_path) as config_file:
            config_data = json.load(config_file)

        return config_data

    def store(self):
        """Store Trakt configurations at ``CONFIG_PATH``
        """
        config = dict(
            CLIENT_ID=self.CLIENT_ID,
            CLIENT_SECRET=self.CLIENT_SECRET,
            OAUTH_TOKEN=self.OAUTH_TOKEN,
            OAUTH_REFRESH=self.OAUTH_REFRESH,
            OAUTH_EXPIRES_AT=self.OAUTH_EXPIRES_AT,
        )

        with open(self.config_path, 'w') as config_file:
            json.dump(config, config_file)
