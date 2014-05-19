"""A wrapper for the Trakt.tv REST API"""
import requests
__author__ = 'Jon Nappi'
__all__ = ['api_key', 'BaseAPI']


@property
def api_key():
    return globals()['_APIKEY_']
@api_key.setter
def api_key(value):
    globals()['_APIKEY_'] = value
@api_key.deleter
def api_key():
    globals()['_APIKEY_'] = None

@property
def server_time():
    """Get the current timestamp (PST) trakt server."""
    url = BaseAPI().base_url + '/server/time.json/{}'.format(api_key)
    response = requests.get(url)
    return response['timestamp']


class BaseAPI(object):
    """Base class containing all basic functionality of a Trakt.tv API call"""
    def __init__(self):
        super(BaseAPI, self).__init__()
        self.base_url = 'http://api.trakt.tv/'

if __name__ == '__main__':
    api_key = '888dbf16c37694fd8633f0f7e423dfc5'
    print api_key
