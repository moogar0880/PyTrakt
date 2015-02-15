"""A wrapper for the Trakt.tv REST API"""
try:
    from ._core import *
except ImportError:
    pass

version_info = (1, 0, 1)
__author__ = 'Jon Nappi'
__version__ = '.'.join([str(i) for i in version_info])


@property
def api_key():
    """The current api key for accessing the Trakt.tv REST API system"""
    if '_TRAKT_APIKEY_' not in globals():
        globals()['_TRAKT_APIKEY_'] = None
    return globals()['_TRAKT_APIKEY_']
@api_key.setter
def api_key(value):
    globals()['_TRAKT_APIKEY_'] = value
@api_key.deleter
def api_key():
    globals()['_TRAKT_APIKEY_'] = None
