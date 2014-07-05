"""Interfaces to all of the Movie objects offered by the Trakt.tv API"""
import json
import requests
from datetime import datetime

from proxy_tools import module_property

from . import BaseAPI, auth_post, Genre, Comment, __version__
import trakt

__author__ = 'Jon Nappi'
__all__ = ['Movie', 'updated_movies', 'rate_movies', 'dismiss_recommendation',
           'get_recommended_movies']


def dismiss_recommendation(imdb_id=None, tmdb_id=None, title=None, year=None):
    """Dismiss the movie matching the specified criteria from showing up in
    recommendations.
    """
    ext = 'recommendations/movies/dismiss/{}'.format(trakt.api_key)
    url = BaseAPI().base_url + ext
    args = {'imdb_id': imdb_id, 'tmdb_id': tmdb_id, 'title': title,
            'year': year}
    real_args = {x: args[x] for x in args if args[x] is not None}
    auth_post(url, real_args)


def get_recommended_movies(genre=None, start_year=None, end_year=None,
                           hide_collected=True, hide_watchlisted=True):
    """Get a list of :class:`Movie`'s recommended based on your watching
    history and your friends. Results are returned with the top recommendation
    first.

    :param genre: Genre slug to filter by. See movies.genres for a list of valid
        genres.
    :param start_year: 4 digit year to filter movies released in this year or
        later.
    :param end_year: 4 digit year to filter movies released in this year or
        earlier.
    :param hide_collected: Set to False to show movies the user has collected.
    :param hide_watchlisted: Set to False to show movies on the user's watchlist
    """
    ext = 'recommendations/movies/{}'.format(trakt.api_key)
    url = BaseAPI().base_url + ext
    if isinstance(genre, Genre):
        slug = genre.slug
    else:
        slug = genre
    args = {'genre': slug, 'start_year': start_year, 'end_year': end_year,
            'hide_collected': hide_collected,
            'hide_watchlisted': hide_watchlisted}
    real_args = {x: args[x] for x in args if args[x] is not None}
    response = auth_post(url, real_args)
    data = json.loads(response.content.decode('UTF-8', 'ignore'))
    movies = []
    for movie in data:
        movies.append(Movie(**movie))
    return movies


def rate_movies(movies, rating):
    """Apply *rating* to all :class:`Movie`'s in *movies*

    :param movies: A `list` of :class:`Movie` objects to rate
    :param rating: The rating to apply to *movies*
    """
    valid_ratings = ['love', 'hate', 'unrate'] + list(range(11))
    if rating in valid_ratings:
        ext = 'rate/movies/{}'.format(trakt.api_key)
        url = BaseAPI().base_url + ext
        movie_list = []
        for movie in movies:
            d = {'imdb_id': movie.imdb_id, 'title': movie.title,
                 'year': movie.year, 'rating': rating}
            movie_list.append(d)
        args = {'movies': movie_list}
        auth_post(url, args)


@module_property
def genres():
    """A list of all possible :class:`Movie` Genres"""
    url = BaseAPI().base_url + '/genres/movies.json/{}'.format(trakt.api_key)
    response = requests.get(url)
    data = json.loads(response.content.decode('UTF-8'))
    genre_list = []
    for genre in data:
        genre_list.append(Genre(genre['name'], genre['slug']))
    return genre_list


@module_property
def trending_movies():
    """All :class:`Movie`'s being watched right now"""
    url = BaseAPI().base_url + '/movies/trending.json/{}'.format(trakt.api_key)
    response = requests.get(url)
    data = json.loads(response.content.decode('UTF-8', 'ignore'))
    to_ret = []
    for movie in data:
        to_ret.append(Movie(**movie))
    return to_ret


def updated_movies(timestamp=None):
    """Returns all movies updated since a timestamp. The server time is in PST.
    To establish a baseline timestamp, you can use the server/time method. It's
    recommended to store the timestamp so you can be efficient in using this
    method.
    """
    ts = timestamp or trakt.server_time
    url = BaseAPI().base_url + '/movies/updated.json/{}/{}'
    url = url.format(trakt.api_key, ts)
    response = requests.get(url)
    data = json.loads(response.content.decode('UTF-8', 'ignore'))
    to_ret = []
    for movie in data['movies']:
        to_ret.append(Movie(**movie))
    return to_ret


class Movie(BaseAPI):
    """A Class representing a Movie object"""
    def __init__(self, title, year=None, **kwargs):
        super(Movie, self).__init__()
        self.title = title
        self.year = int(year) if year is not None else year
        self.released_iso = self.tmdb_id = self.imdb_id = self.duration = None
        self.url = self._comments = self.genres = self.certification = None
        self.overview = None
        self.url_extension = 'search/movies/{}?query='.format(trakt.api_key)
        self._checked_in = False
        self.images = {}
        if len(kwargs) > 0:
            self._build(kwargs)
        else:
            self._search(self.title)

    def _search(self, title):
        """Perform a search for the specified *title*

        :param title: The title to search for
        """
        query = title.replace(' ', '%20')
        ext = self.url_extension + query
        data = self._get_(ext)
        if data is not None and self.year is not None:
            for movie in data:
                title = movie['title'].lower()
                if movie['year'] == self.year and title == self.title.lower():
                    data = movie
                    break
            if isinstance(data, list):
                data = data[0]
        elif data is not None and self.year is None:
            data = data[0]
        if data is not None and data != []:
            self._build(data)
        try:
            release = getattr(self, 'released')
            release = float(release)
            utc = datetime.utcfromtimestamp(release)
            self.released_iso = str(utc).replace(' ', 'T')
        except AttributeError:
            pass

    def _build(self, data):
        """Build this :class:`Movie` object with the data in *data*"""
        for key, val in data.items():
            if key == 'genres':
                self.genres = []
                for genre in val:
                    slug = genre.lower().replace(' ', '-')
                    self.genres.append(Genre(genre, slug))
            else:
                setattr(self, key, val)

    def checkin(self, venue_id=None, venue_name=None, facebook=False,
                twitter=False, tumblr=False, path=False):
        """Check into this :class:`Movie` on Trakt.tv. Think of this method as
        in between a seen and a scrobble. After checking in, Trakt will
        automatically display it as watching then switch over to watched status
        once the duration has elapsed.

        :param venue_id: Foursquare venue ID
        :param venue_name: Custom venue name for display purposes.
        :param facebook: Flag to share on Facebook
        :param twitter: Flag to share on Twitter
        :param tumblr: Flag to share on tumblr
        :param path: Flag to share on path?
        """
        ext = 'movie/checkin/{}'.format(trakt.api_key)
        share = {'facebook': facebook, 'twitter': twitter, 'tumblr': tumblr,
                 'path': path}
        args = {'app_version': __version__, 'app_date': 'June 4 2011',
                'share': share, 'venue_id': venue_id, 'venue_name': venue_name}
        for key, val in self._generic_json.items():
            args[key] = val
        real_args = {x: args[x] for x in args if args[x] is not None}
        self._post_(ext, real_args)

    def cancel_checkin(self):
        """Notify trakt that the current user is no longer watching this
        :class:`Movie`
        """
        ext = 'movie/cancelcheckin/{}'.format(trakt.api_key)
        self._post_(ext)

    def cancel_watching(self):
        """Notify trakt that the current user has stopped watching this
        :class:`Movie`
        """
        ext = 'movie/cancelwatching/{}'.format(trakt.api_key)
        self._post_(ext)

    def comment(self, comment, spoiler=False, review=False):
        """Add a comment (shout or review) to this :class:`Move` on trakt."""
        ext = '/comment/episode/{}'.format(trakt.api_key)
        args = {'title': self.title, 'year': self.year, 'comment': comment,
                'spoiler': spoiler, 'review': review}
        if self.tmdb_id == '' or self.tmdb_id is None:
            args['imdb_id'] = self.imdb_id
        else:
            args['tmdb_id'] = self.tmdb_id
        self._post_(ext, args)

    def dismiss(self):
        """Dismiss this movie from showing up in Movie Recommendations"""
        dismiss_recommendation(imdb_id=self.imdb_id, tmdb_id=self.tmdb_id,
                               title=self.title, year=self.year)

    def add_to_library(self):
        """Add this :class:`Movie` to your library."""
        ext = 'movie/library/{}'.format(trakt.api_key)
        args = self._generic_json
        del args['duration']
        real_args = {'movies': [args]}
        self._post_(ext, real_args)

    def remove_from_library(self):
        """Remove this :class:`Movie` from your library."""
        ext = 'movie/unlibrary/{}'.format(trakt.api_key)
        args = self._generic_json
        del args['duration']
        real_args = {'movies': [args]}
        self._post_(ext, real_args)

    def add_to_watchlist(self):
        """Add this :class:`Movie` to your watchlist"""
        ext = 'movie/watchlist/{}'.format(trakt.api_key)
        args = {'movies': [{'imdb_id': self.imdb_id, 'title': self.title,
                            'year': self.year}]}
        self._post_(ext, args)

    def start_watching(self, progress, media_center_version, media_center_date):
        """Notify trakt that the current user has started watching this
        :class:`Movie`.

        :param progress: % progress, integer 0-100. It is recommended to call
            the watching API every 15 minutes, then call the scrobble API near
            the end of the movie to lock it in.
        :param media_center_version: Version number of the media center, be as
            specific as you can including nightly build number, etc. Used to
            help debug your plugin.
        :param media_center_date: Build date of the media center. Used to help
            debug your plugin.
        """
        ext = 'movie/watching/{}'.format(trakt.api_key)
        args = {'progress': progress, 'media_center_date': media_center_date,
                'media_center_version': media_center_version,
                'plugin_version': __version__}
        for key, val in self._generic_json.items():
            args[key] = val
        real_args = {x: args[x] for x in args if args[x] is not None}
        self._post_(ext, real_args)

    @property
    def comments(self):
        """All comments (shouts and reviews) for this :class:`Movie`. Most
        recent comments returned first.
        """
        from .users import User
        trakt_title = self.url.split('/')[-1]
        ext = 'movie/comments.json/{}/{}'.format(trakt.api_key, trakt_title)
        data = self._get_(ext)
        self._comments = []
        for comment in data:
            user = User(comment.pop('user'))
            self._comments.append(Comment(user=user, **comment))
        return self._comments

    @property
    def related(self):
        """The top 10 :class:`Movie`'s related to this :class:`Movie`"""
        ext = 'movie/related.format/{}/{}/hidewatched'.format(trakt.api_key,
                                                              self.title)
        response = self._post_(ext)
        data = json.loads(response.content.decode('UTF-8'))
        movies = []
        for movie in data:
            movies.append(Movie(**movie))
        return movies

    def mark_as_seen(self, last_played=None):
        """Add this :class:`Movie`, watched outside of trakt, to your library."""
        ext = 'movie/seen/{}'.format(trakt.api_key)
        args = self._generic_json
        del args['duration']
        if last_played is not None:
            args['last_played'] = last_played
        real_args = {'movies': [args]}
        self._post_(ext, real_args)

    def mark_as_unseen(self):
        """Remove this :class:`Movie`, watched outside of trakt, from your
        library.
        """
        ext = 'movie/unseen/{}'.format(trakt.api_key)
        args = self._generic_json
        del args['duration']
        real_args = {'movies': [args]}
        self._post_(ext, real_args)

    def rate(self, rating):
        """Rate this :class:`Movie` on trakt. Depending on the current users
        settings, this may also send out social updates to facebook, twitter,
        tumblr, and path.
        """
        valid_ratings = ['love', 'hate', 'unrate'] + list(range(11))
        if rating in valid_ratings:
            ext = 'rate/movie/{}'.format(trakt.api_key)
            args = {'rating': rating}
            for key, val in self._generic_json.items():
                if key != 'duration':
                    args[key] = val
            self._post_(ext, args)

    def scrobble(self, progress, media_center_version, media_center_date):
        """Notify trakt that the current user has finished watching a movie.
        This commits this :class:`Movie` to the current users profile. You
        should use movie/watching prior to calling this method.

        :param progress: % progress, integer 0-100. It is recommended to call
            the watching API every 15 minutes, then call the scrobble API near
            the end of the movie to lock it in.
        :param media_center_version: Version number of the media center, be as
            specific as you can including nightly build number, etc. Used to
            help debug your plugin.
        :param media_center_date: Build date of the media center. Used to help
            debug your plugin.
        """
        ext = 'movie/scrobble/{}'.format(trakt.api_key)
        args = {'progress': progress, 'media_center_date': media_center_date,
                'media_center_version': media_center_version,
                'plugin_version': __version__}
        for key, val in self._generic_json.items():
            args[key] = val
        real_args = {x: args[x] for x in args if args[x] is not None}
        self._post_(ext, real_args)

    def watching(self, progress, media_center_version, media_center_date):
        """Check into this :class:`Movie` on Trakt.tv. Think of this method as
        in between a seen and a scrobble. After checking in, Trakt will
        automatically display it as watching then switch over to watched status
        once the duration has elapsed.

        :param progress: % progress, integer 0-100. It is recommended to call
            the watching API every 15 minutes, then call the scrobble API near
            the end of the movie to lock it in.
        :param media_center_version: Version number of the media center, be as
            specific as you can including nightly build number, etc. Used to
            help debug your plugin.
        :param media_center_date: Build date of the media center. Used to help
            debug your plugin.
        """
        ext = 'movie/checkin/{}'.format(trakt.api_key)
        args = {'progress': progress, 'media_center_date': media_center_date,
                'media_center_version': media_center_version,
                'plugin_version': __version__}
        for key, val in self._generic_json.items():
            args[key] = val
        real_args = {x: args[x] for x in args if args[x] is not None}
        self._post_(ext, real_args)

    @property
    def watching_now(self):
        """A list of all :class:`User`'s watching a movie."""
        from .users import User
        ext = 'movie/watchingnow.json/{}/{}'.format(trakt.api_key, self.imdb_id)
        data = self._post_(ext)
        users = []
        for user in data:
            users.append(User(**user))
        return users

    @property
    def _list_json(self):
        """The JSON representation of this :class:`Movie` needed for adding it
        into a :class:`UserList`
        """
        return {'type': 'movie', 'imdb_id': self.imdb_id, 'title': self.title,
                'year': self.year}

    @property
    def _generic_json(self):
        """"""
        return {'imdb_id': self.imdb_id, 'title': self.title, 'year': self.year,
                'duration': self.duration}

    def __str__(self):
        """String representation of a :class:`Movie`"""
        return '<Movie>: {}'.format(self.title.encode('ascii', 'ignore'))
    __repr__ = __str__
