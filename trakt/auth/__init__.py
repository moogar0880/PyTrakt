# -*- coding: utf-8 -*-
"""Authentication methods"""

__author__ = 'Jon Nappi, Elan Ruusamäe'

from trakt import PIN_AUTH, OAUTH_AUTH, DEVICE_AUTH


def pin_auth():
    pass


def oauth_auth():
    pass


def device_auth(*args, **kwargs):
    from trakt.auth.device import DeviceAuth

    return DeviceAuth(*args, **kwargs).authenticate()


def init_auth(method: str, *args, **kwargs):
    methods = {
        PIN_AUTH: pin_auth, OAUTH_AUTH: oauth_auth, DEVICE_AUTH: device_auth
    }

    """Run the auth function specified by *AUTH_METHOD*"""
    return methods.get(method, PIN_AUTH)(*args, **kwargs)
