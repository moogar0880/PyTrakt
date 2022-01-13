# -*- coding: utf-8 -*-
"""Authentication methods"""

__author__ = 'Jon Nappi, Elan Ruusamäe'

from trakt import PIN_AUTH, OAUTH_AUTH, DEVICE_AUTH


def pin_auth():
    pass


def oauth_auth():
    pass


def device_auth():
    pass


def init(AUTH_METHOD, *args, **kwargs):
    auth_method = {
        PIN_AUTH: pin_auth, OAUTH_AUTH: oauth_auth, DEVICE_AUTH: device_auth
    }

    """Run the auth function specified by *AUTH_METHOD*"""
    return auth_method.get(AUTH_METHOD, PIN_AUTH)(*args, **kwargs)
