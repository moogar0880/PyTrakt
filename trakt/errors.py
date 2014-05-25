"""Misc Trakt related errors"""
__author__ = 'Jon Nappi'
__all__ = ['TraktException', 'InvalidAPIKey', 'InvalidCredentials']


class TraktException(BaseException):
    pass


class InvalidAPIKey(TraktException):
    pass


class InvalidCredentials(TraktException):
    pass
