"""Interfaces to all of the Movie objects offered by the Trakt.tv API"""
import json
import string
import requests
from datetime import datetime, timedelta
from collections import namedtuple

from . import api_key, BaseAPI, auth_post, __version__
from trakt.user import User

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

@property
def genres():
    """A list of all possible :class:`Movie` Genres"""
    Genre = namedtuple('Genre', ['name', 'slug'])
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
        self.url_extension = 'search/movies/' + api_key + '?query='
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

    def add_to_watchlist(self):
        """Add this :class:`Movie` to your watchlist"""
        ext = '/movie/watchlist/{}'.format(api_key)
        url = self.base_url + ext
        args = {'movies': [{'imdb_id': self.imdb_id, 'title': self.title,
                            'year': self.year}]}
        auth_post(url, args)

    def start_watching(self):
        """"""
        ext = '/movie/watching/{}'.format(api_key)
        url = self.base_url + ext
        raise NotImplemented

    @property
    def comments(self):
        """All comments (shouts and reviews) for this :class:`Movie`. Most
        recent comments returned first.
        """
        Comment = namedtuple('Comment', ['id', 'inserted', 'text', 'text_html',
                                         'spoiler', 'type', 'likes', 'replies',
                                         'user', 'user_ratings'])
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
