# -*- coding: utf-8 -*-
"""trakt.tv functional tests"""
from trakt.api import TraktApi
from trakt.core import api
from trakt.tv import TVShow


def test_api():
    api1 = api()
    api2 = api()
    assert isinstance(api1, TraktApi)
    assert api1 == api2

    show = TVShow('Game of Thrones')
    assert show.title == 'Game of Thrones'
