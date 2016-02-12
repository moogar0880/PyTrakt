"""A wrapper for the Trakt.tv REST API"""
try:
    from .core import *
except ImportError:
    pass

version_info = (2, 3, 0)
__author__ = 'Jon Nappi'
__version__ = '.'.join([str(i) for i in version_info])
