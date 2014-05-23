"""Interfaces to all of the Movie objects offered by the Trakt.tv API"""
import json
import string
import requests
from datetime import datetime, timedelta

from . import api_key, BaseAPI, auth_post, Genre, Comment, __version__
from trakt.users import User

__author__ = 'Jon Nappi'
__all__ = ['Movie', 'trending_movies', 'updated_movies']


def dismiss_recommendation(imdb_id=None, tmdb_id=None, title=None, year=None):
    """Dismiss the movie matching the specified criteria from showing up in
    recommendations.
    """
    ext = '/recommendations/movies/dismiss/{}'.format(api_key)
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
    ext = '/recommendations/movies/{}'.format(api_key)
    url = BaseAPI().base_url + ext
    args = {'genre': genre, 'start_year': start_year, 'end_year': end_year,
            'hide_collected': hide_collected,
            'hide_watchlisted': hide_watchlisted}
    real_args = {x: args[x] for x in args if args[x] is not None}
    response = auth_post(url, real_args)
    movies = []
    for movie in response:
        movies.append(Movie(**movie))
    return movies


def rate_movies(movies, rating):
    """Apply *rating* to all :class:`Movie`'s in *movies*

    :param movies: A `list` of :class:`Movie` objects to rate
    :param rating: The rating to apply to *movies*
    """
    valid_ratings = ['love', 'hate', 'unrate'] + list(range(11))
    if rating in valid_ratings:
        ext = '/rate/movies/{}'.format(api_key)
        url = BaseAPI().base_url + ext
        movie_list = []
        for movie in movies:
            d = {'imdb_id': movie.imdb_id, 'title': movie.title,
                 'year': movie.year, 'rating': rating}
            movie_list.append(d)
        args = {'movies': movie_list}
        auth_post(url, args)

@property
def genres():
    """A list of all possible :class:`Movie` Genres"""
    url = BaseAPI().base_url + '/genres/movies.json/{}'.format(api_key)
    response = requests.get(url)
    data = json.loads(response.content.decode('UTF-8'))
    genre_list = []
    for genre in data:
        genre_list.append(Genre(genre['name'], genre['slug']))
    return genre_list


@property
def trending_movies():
    """All :class:`Movie`'s being watched right now"""
    url = BaseAPI().base_url + '/movies/trending.json/{}'.format(api_key)
    response = requests.get(url)
    data = json.loads(response.content.decode('UTF-8'))
    to_ret = []
    for movie in data:
        title = movie.get('title')
        to_ret.append(Movie(title, **movie))
    return to_ret


def updated_movies(timestamp=None):
    """Returns all movies updated since a timestamp. The server time is in PST.
    To establish a baseline timestamp, you can use the server/time method. It's
    recommended to store the timestamp so you can be efficient in using this
    method.
    """
    y_day = datetime.now() - timedelta(1)
    ts = timestamp or int(y_day.strftime('%s')) * 1000
    url = BaseAPI().base_url + '/movies/updated.json/{}/{}'.format(api_key, ts)
    response = requests.get(url)
    data = json.loads(response.content.decode('UTF-8'))
    return data['movies']


class Movie(BaseAPI):
    """A Class representing a Movie object"""
    def __init__(self, title, year=None, **kwargs):
        super(Movie, self).__init__()
        self.title = title
        self.year = int(year)
        self.released_iso = self.tmdb_id = self.imdb_id = self.duration = None
        self.url_extension = 'search/movies/{}?query='.format(api_key)
        self._checked_in = False
        if len(kwargs) > 0:
            for key, val in kwargs.items():
                setattr(self, key, val)
        else:
            self.search(self.title)

    def search(self, title):
        query = string.replace(title, ' ', '%20')
        url = self.base_url + self.url_extension + query
        response = requests.get(url)
        data = None
        if response.status_code == 200:
            data = json.loads(response.content)
            if data is not None and self.year is not None:
                for movie in data:
                    title = movie['title'].lower()
                    # print title, self.title.lower()
                    # print movie['year'], self.year, movie['year'] == self.year
                    if movie['year'] == self.year and title == self.title.lower():
                        data = movie
                        break
                if isinstance(data, list):
                    data = data[0]
            elif data is not None and self.year is None:
                data = data[0]
            # print data
            if data is not None and data != []:
                for key, val in data.items():
                    setattr(self, key, val)
            try:
                release = getattr(self, 'released')
                release = float(release)
                utc = datetime.utcfromtimestamp(release)
                self.released_iso = str(utc).replace(' ', 'T')
            except AttributeError:
                pass

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
        ext = '/movie/checkin/{}'.format(api_key)
        url = self.base_url + ext
        share = {'facebook': facebook, 'twitter': twitter, 'tumblr': tumblr,
                 'path': path}
        args = {'app_version': __version__, 'app_date': 'June 4 2011',
                'share': share, 'venue_id': venue_id, 'venue_name': venue_name}
        for key, val in self._generic_json.items():
            args[key] = val
        real_args = {x: args[x] for x in args if args[x] is not None}
        auth_post(url, real_args)

    def cancel_checkin(self):
        """Notify trakt that the current user is no longer watching this
        :class:`Movie`
        """
        ext = '/movie/cancelcheckin/{}'.format(api_key)
        url = self.base_url + ext
        auth_post(url)

    def cancel_watching(self):
        """Notify trakt that the current user has stopped watching this
        :class:`Movie`
        """
        ext = '/movie/cancelwatching/{}'.format(api_key)
        url = self.base_url + ext
        auth_post(url)

    def comment(self, comment, spoiler=False, review=False):
        """Add a comment (shout or review) to this :class:`Move` on trakt."""
        url = self.base_url + '/comment/episode/{}'.format(api_key)
        args = {'title': self.title, 'year': self.year, 'comment': comment,
                'spoiler': spoiler, 'review': review}
        if self.tmdb_id == '' or self.tmdb_id is None:
            args['imdb_id'] = self.imdb_id
        else:
            args['tmdb_id'] = self.tmdb_id
        auth_post(url, kwargs=args)

    def dismiss(self):
        """Dismiss this movie from showing up in Movie Recommendations"""
        dismiss_recommendation(imdb_id=self.imdb_id, tmdb_id=self.tmdb_id,
                               title=self.title, year=self.year)

    def add_to_library(self):
        """Add this :class:`Movie` to your library."""
        ext = '/movie/library/{}'.format(api_key)
        url = self.base_url + ext
        args = self._generic_json
        del args['duration']
        real_args = {'movies': [args]}
        auth_post(url, real_args)

    def remove_from_library(self):
        """Remove this :class:`Movie` from your library."""
        ext = '/movie/unlibrary/{}'.format(api_key)
        url = self.base_url + ext
        args = self._generic_json
        del args['duration']
        real_args = {'movies': [args]}
        auth_post(url, real_args)

    def add_to_watchlist(self):
        """Add this :class:`Movie` to your watchlist"""
        ext = '/movie/watchlist/{}'.format(api_key)
        url = self.base_url + ext
        args = {'movies': [{'imdb_id': self.imdb_id, 'title': self.title,
                            'year': self.year}]}
        auth_post(url, args)

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
        ext = '/movie/watching/{}'.format(api_key)
        url = self.base_url + ext
        args = {'progress': progress, 'media_center_date': media_center_date,
                'media_center_version': media_center_version,
                'plugin_version': __version__}
        for key, val in self._generic_json.items():
            args[key] = val
        real_args = {x: args[x] for x in args if args[x] is not None}
        auth_post(url, real_args)

    @property
    def comments(self):
        """All comments (shouts and reviews) for this :class:`Movie`. Most
        recent comments returned first.
        """
        ext = '/movie/comments.json/{}/{}'.format(api_key, self.title)
        url = self.base_url + ext
        response = requests.get(url)
        data = json.loads(response.content.decode('UTF-8'))
        comments = []
        for comment in data:
            user = User(**comment.get('user'))
            ratings = comment.get('user_ratings')
            comments.append(Comment(user=user, user_ratings=ratings, **comment))
        return comments

    @property
    def related(self):
        """The top 10 :class:`Movie`'s related to this :class:`Movie`"""
        ext = '/movie/related.format/{}/{}/hidewatched'.format(api_key,
                                                               self.title)
        url = self.base_url + ext
        response = auth_post(url)
        data = json.loads(response.content.decode('UTF-8'))
        movies = []
        for movie in data:
            movies.append(Movie(**movie))
        return movies

    def mark_as_seen(self, last_played=None):
        """Add this :class:`Movie`, watched outside of trakt, to your library."""
        ext = '/movie/seen/{}'.format(api_key)
        url = self.base_url + ext
        args = self._generic_json
        del args['duration']
        if last_played is not None:
            args['last_played'] = last_played
        real_args = {'movies': [args]}
        auth_post(url, real_args)

    def mark_as_unseen(self):
        """Remove this :class:`Movie`, watched outside of trakt, from your
        library.
        """
        ext = '/movie/unseen/{}'.format(api_key)
        url = self.base_url + ext
        args = self._generic_json
        del args['duration']
        real_args = {'movies': [args]}
        auth_post(url, real_args)

    def rate(self, rating):
        """Rate this :class:`Movie` on trakt. Depending on the current users
        settings, this may also send out social updates to facebook, twitter,
        tumblr, and path.
        """
        valid_ratings = ['love', 'hate', 'unrate'] + list(range(11))
        if rating in valid_ratings:
            ext = '/rate/movie/{}'.format(api_key)
            url = self.base_url + ext
            args = {'rating': rating}
            for key, val in self._generic_json.items():
                if key != 'duration':
                    args[key] = val
            auth_post(url, args)

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
        ext = '/movie/scrobble/{}'.format(api_key)
        url = self.base_url + ext
        args = {'progress': progress, 'media_center_date': media_center_date,
                'media_center_version': media_center_version,
                'plugin_version': __version__}
        for key, val in self._generic_json.items():
            args[key] = val
        real_args = {x: args[x] for x in args if args[x] is not None}
        auth_post(url, real_args)

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
        ext = '/movie/checkin/{}'.format(api_key)
        url = self.base_url + ext
        args = {'progress': progress, 'media_center_date': media_center_date,
                'media_center_version': media_center_version,
                'plugin_version': __version__}
        for key, val in self._generic_json.items():
            args[key] = val
        real_args = {x: args[x] for x in args if args[x] is not None}
        auth_post(url, real_args)

    @property
    def watching_now(self):
        """A list of all :class:`User`'s watching a movie."""
        ext = '/movie/watchingnow.json/{}/{}'.format(api_key, self.imdb_id)
        url = self.base_url + ext
        response = auth_post(url)
        data = json.loads(response.content.decode('UTF-8'))
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
