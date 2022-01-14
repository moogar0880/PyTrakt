# -*- coding: utf-8 -*-
"""Authentication methods"""

__author__ = 'Jon Nappi, Elan Ruusamäe'

from trakt import PIN_AUTH, OAUTH_AUTH, DEVICE_AUTH, api, config


def pin_auth(*args, **kwargs):
    from trakt.auth.pin import PinAuth

    return PinAuth(*args, client=api(), config=config(), **kwargs).authenticate()


def oauth_auth(*args, **kwargs):
    from trakt.auth.oauth import OAuth

    return OAuth(*args, client=api(), config=config(), **kwargs).authenticate()


def device_auth(*args, **kwargs):
    from trakt.auth.device import DeviceAuth

    return DeviceAuth(*args, client=api(), config=config(), **kwargs).authenticate()


def get_client_info(app_id=False):
    """Helper function to poll the user for Client ID and Client Secret
    strings

    :return: A 2-tuple of client_id, client_secret
    """
    global APPLICATION_ID
    print('If you do not have a client ID and secret. Please visit the '
          'following url to create them.')
    print('http://trakt.tv/oauth/applications')
    client_id = input('Please enter your client id: ')
    client_secret = input('Please enter your client secret: ')
    if app_id:
        msg = 'Please enter your application ID ({default}): '.format(
            default=APPLICATION_ID)
        user_input = input(msg)
        if user_input:
            APPLICATION_ID = user_input
    return client_id, client_secret


def _store(**kwargs):
    from trakt.core import config

    config().store(**kwargs)


def init_auth(method: str, *args, **kwargs):
    """Run the auth function specified by *AUTH_METHOD*"""

    methods = {
        PIN_AUTH: pin_auth,
        OAUTH_AUTH: oauth_auth,
        DEVICE_AUTH: device_auth,
    }

    return methods.get(method, PIN_AUTH)(*args, **kwargs)
