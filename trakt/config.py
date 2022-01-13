# -*- coding: utf-8 -*-
"""Class for config loading/storing"""

__author__ = 'Elan Ruusamäe'

import json
from os.path import exists


class Config:
    def __init__(self, config_path: str):
        self.config_path = config_path

    def exists(self):
        return exists(self.config_path)

    def store(self, **kwargs):
        """Helper function used to store Trakt configurations at ``CONFIG_PATH``

        :param kwargs: Keyword args to store at ``CONFIG_PATH``
        """
        with open(self.config_path, 'w') as config_file:
            json.dump(kwargs, config_file)
