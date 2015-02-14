# -*- coding: utf-8 -*-
import collections

from ._core import get, post, BaseAPI

__author__ = 'Jon Nappi'


@post
def comment(media, comment_body, spoiler=False, review=False):
    if not review and len(comment_body) > 200:
        review = True
    data = dict(comment=comment_body, spoiler=spoiler, review=review)
    data.update(media.to_json())
    return 'comments', data


@post
def rate(media, rating):
    if not isinstance(media, collections.Iterable):
        media = [media]  # Figure out how the hell to process this data
    data = dict(rating=rating)
    data.update(media.to_json())
    return 'sync/ratings', data


@post
def add_to_history(media, watched_at):
    pass


@post
def add_to_watchlist(media):
    pass


@post
def remove_from_history(media):
    pass


@post
def remove_from_watchlist(media):
    pass


@post
def add_to_collection(media):
    pass


@post
def remove_from_collection(media):
    pass


@get
def search(query, search_type='movie'):
    valids = ('movie', 'show', 'episode', 'person', 'list')
    if search_type not in valids:
        raise ValueError('search_type must be one of {}'.format(valids))
    data = yield 'search?query={query}&type={type}'.format(query=query,
                                                           type=search_type)
    yield data


class Scrobbler(BaseAPI):
    def __init__(self, media, progress, app_version, app_date):
        super(Scrobbler, self).__init__()
        self.progress, self.version = progress, app_version
        self.media, self.date = media, app_date
        if self.progress > 0:
            self.start()

    def start(self):
        self._post_('scrobble/start')

    def pause(self):
        self._post_('scrobble/pause')

    def stop(self):
        self._post_('scrobble/stop')

    def finish(self):
        if self.progress < 80.0:
            self.progress = 100.0
        self.stop()

    def update(self, progress):
        self.progress = progress
        self.start()

    def _post_(self, uri, args=None):
        payload = dict(progress=self.progress, app_version=self.version,
                       date=self.date)
        payload.update(self.media.to_json())
        super(Scrobbler, self)._post_(uri, payload)

    def __enter__(self):
        self.start()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.finish()
