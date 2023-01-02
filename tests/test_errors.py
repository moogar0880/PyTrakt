# -*- coding: utf-8 -*-
"""unit tests to define behavior of custom exception types"""
from trakt.errors import (BadRequestException, ConflictException,
                          ForbiddenException, NotFoundException,
                          OAuthException, ProcessException, RateLimitException,
                          TraktException, TraktInternalException,
                          TraktUnavailable)


def test_trakt_exception():
    texc = TraktException()
    assert texc.http_code is None
    assert texc.message is None


def test_400_exception():
    texc = BadRequestException()
    assert texc.http_code == 400
    assert texc.message == "Bad Request - request couldn't be parsed"
    assert str(texc) == texc.message


def test_401_exception():
    texc = OAuthException()
    assert texc.http_code == 401
    assert texc.message == 'Unauthorized - OAuth must be provided'
    assert str(texc) == texc.message


def test_403_exception():
    texc = ForbiddenException()
    assert texc.http_code == 403
    assert texc.message == 'Forbidden - invalid API key or unapproved app'
    assert str(texc) == texc.message


def test_404_exception():
    texc = NotFoundException()
    assert texc.http_code == 404
    assert texc.message == 'Not Found - method exists, but no record found'
    assert str(texc) == texc.message


def test_409_exception():
    texc = ConflictException()
    assert texc.http_code == 409
    assert texc.message == 'Conflict - resource already created'
    assert str(texc) == texc.message


def test_422_exception():
    texc = ProcessException()
    assert texc.http_code == 422
    assert texc.message == 'Unprocessable Entity - validation errors'
    assert str(texc) == texc.message


def test_429_exception():
    texc = RateLimitException()
    assert texc.http_code == 429
    assert texc.message == 'Rate Limit Exceeded'
    assert str(texc) == texc.message


def test_500_exception():
    texc = TraktInternalException()
    assert texc.http_code == 500
    assert texc.message == 'Internal Server Error'
    assert str(texc) == texc.message


def test_503_exception():
    texc = TraktUnavailable()
    assert texc.http_code == 503
    assert texc.message == 'Trakt Unavailable - server overloaded'
    assert str(texc) == texc.message
