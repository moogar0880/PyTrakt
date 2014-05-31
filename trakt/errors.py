"""Misc Trakt related errors"""
__author__ = 'Jon Nappi'
__all__ = ['TraktException', 'InvalidAPIKey', 'InvalidCredentials']


class TraktException(BaseException):
    """Base Exception type for trakt module"""
    pass


class InvalidAPIKey(TraktException):
    """Custom trakt exception to be raised if the provided API Key is invalid"""
    pass


class InvalidCredentials(TraktException):
    """Custom trakt exception to be raised if a provided username and password
    are determined to be invalid
    """
    pass
