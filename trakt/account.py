"""Interfaces to all of the Account objects offered by the Trakt.tv API"""
import json
import requests
from hashlib import sha1

from . import BaseAPI
import trakt
__author__ = 'Jon Nappi'
__all__ = ['create_account', 'settings', 'test']


def create_account(username, password, email):
    """Create a new trakt account. Username and e-mail must be unique and not
    already exist in trakt.
    """
    hex_pass = sha1(password.encode('UTF-8')).hexdigest()
    args = {'username': username, 'password': hex_pass, 'email': email}
    url = BaseAPI().base_url + 'account/create/{}'.format(trakt.api_key)
    response = requests.post(url, data=args)
    resp_data = json.loads(response.content.decode('UTF-8'))
    return resp_data


def settings(username, password):
    """Returns all settings for the authenticated user. Use these settings to
    customize your app based on the user's settings. For example, if they use
    advanced ratings show a 10 heart scale. If they prefer simple ratings, show
    the binary scale. The social connections are also useful to customize the
    checkin prompt.
    """
    hex_pass = sha1(password.encode('UTF-8')).hexdigest()
    args = {'username': username, 'password': hex_pass}
    url = BaseAPI().base_url + 'account/settings/{}'.format(trakt.api_key)
    response = requests.post(url, data=args)
    resp_data = json.loads(response.content.decode('UTF-8'))
    return resp_data


def test(username, password):
    """Test trakt credentials. This is useful for your configuration screen and
    is a simple way to test someone's trakt account.
    """
    hex_pass = sha1(password.encode('UTF-8')).hexdigest()
    args = {'username': username, 'password': hex_pass}
    url = BaseAPI().base_url + 'account/test/{}'.format(trakt.api_key)
    response = requests.post(url, data=args)
    resp_data = json.loads(response.content.decode('UTF-8'))
    return resp_data['status'] == 'success'
