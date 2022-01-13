# -*- coding: utf-8 -*-
"""trakt.tv functional tests"""
from trakt.api import HttpClient
from trakt.core import api, Alias
from trakt.tv import TVShow


def test_api():
    api1 = api()
    api2 = api()
    assert isinstance(api1, HttpClient)
    assert api1 == api2

    show = TVShow('Game of Thrones')
    assert show.title == 'Game of Thrones'
    assert show.certification == 'TV-MA'