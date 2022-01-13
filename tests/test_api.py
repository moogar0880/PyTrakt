# -*- coding: utf-8 -*-
"""trakt.tv functional tests"""
from trakt.api import TraktApi
from trakt.core import get_api
from trakt.tv import TVShow


def test_api():
    api = get_api()
    assert isinstance(api, TraktApi)

    show = TVShow('Game of Thrones')
    assert show.title == 'Game of Thrones'
