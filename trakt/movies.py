"""Interfaces to all of the Movie objects offered by the Trakt.tv API"""
from collections import namedtuple

from .sync import (Scrobbler, comment, rate, add_to_history,
                   remove_from_history, add_to_watchlist,
                   remove_from_watchlist, add_to_collection,
                   remove_from_collection, search)
from ._core import BaseAPI, Alias, Comment, Genre, Translation, get, delete
from .utils import slugify, now, extract_ids
from .people import Person

__author__ = 'Jon Nappi'
__all__ = ['Movie', 'updated_movies', 'rate_movies', 'dismiss_recommendation',
           'get_recommended_movies', 'genres', 'trending_movies']


@delete
def dismiss_recommendation(title):
    """Dismiss the movie matching the specified criteria from showing up in
    recommendations.
    """
    return 'recommendations/movies/{title}'.format(title=title)


@get
def get_recommended_movies():
    """Get a list of :class:`Movie`'s recommended based on your watching
    history and your friends. Results are returned with the top recommendation
    first.
    """
    data = yield 'recommendations/movies'
    movies = []
    for movie in data:
        extract_ids(movie)
        movies.append(Movie(**movie))
    yield movies


@get
def genres():
    """A list of all possible :class:`Movie` Genres"""
    data = yield 'genres/movies'
    yield [Genre(g['name'], g['slug']) for g in data]


@get
def trending_movies():
    """All :class:`Movie`'s being watched right now"""
    data = yield '/movies/trending'
    to_ret = []
    for movie in data:
        watchers = movie.pop('watchers')
        to_ret.append(Movie(watchers=watchers, **movie.pop('movie')))
    yield to_ret


@get
def updated_movies(timestamp=None):
    """Returns all movies updated since a timestamp. The server time is in PST.
    To establish a baseline timestamp, you can use the server/time method. It's
    recommended to store the timestamp so you can be efficient in using this
    method.
    """
    ts = timestamp or now()
    data = yield 'movies/updates/{start_date}'.format(start_date=ts)
    to_ret = []
    for movie in data:
        mov = movie.pop('movie')
        extract_ids(mov)
        mov.update({'updated_at': movie.pop('updated_at')})
        to_ret.append(Movie(**mov))
    yield to_ret


Release = namedtuple('Release', ['country', 'certification', 'release_date'])


class Movie(BaseAPI):
    """A Class representing a Movie object"""
    def __init__(self, title, year=None, **kwargs):
        super(Movie, self).__init__()
        self.title = title
        self.year = int(year) if year is not None else year
        if self.year is not None:
            self.slug = slugify('-'.join([self.title, str(self.year)]))
        else:
            self.slug = slugify(self.title)

        self.released = self.tmdb_id = self.imdb_id = self.duration = None
        self.trakt_id = self.tagline = self.overview = self.runtime = None
        self.updated_at = self.trailer = self.homepage = self.rating = None
        self.votes = self.language = self.available_translations = None
        self.genres = self.certification = None
        self._comments = self._images = self._aliases = self._people = None
        self._ratings = None

        if len(kwargs) > 0:
            self._build(kwargs)
        else:
            self._build(self._get_(self.ext_full))

    @classmethod
    def search(cls, title):
        """Perform a search for the specified *title*

        :param title: The title to search for
        """
        return search(title, search_type='movie')

    def _build(self, data):
        """Build this :class:`Movie` object with the data in *data*"""
        extract_ids(data)
        for key, val in data.items():
            setattr(self, key, val)

    @property
    def ext(self):
        """Base uri to retrieve basic information about this :class:`Movie`"""
        return 'movies/{slug}'.format(slug=self.slug)

    @property
    def ext_full(self):
        """Uri to retrieve all information about this :class:`Movie`"""
        return self.ext + '?extended=full'

    @property
    def images_ext(self):
        """Uri to retrieve additional image information"""
        return self.ext + '?extended=images'

    @property
    def aliases(self):
        """A list of :class:`Alias` objects representing all of the other
        titles that this :class:`Movie` is known by, and the countries where
        they go by their alternate titles
        """
        if self._aliases is None:
            data = self._get_(self.ext + '/aliases')
            self._aliases = [Alias(**alias) for alias in data]
        return self._aliases

    @property
    def cast(self):
        """All of the cast members that worked on this :class:`Movie`"""
        return [p for p in self.people if getattr(p, 'character')]

    @property
    def comments(self):
        """All comments (shouts and reviews) for this :class:`Movie`. Most
        recent comments returned first.
        """
        # TODO (jnappi) Pagination
        from .users import User
        ext = self.ext + '/comments'
        data = self._get_(ext)
        self._comments = []
        for com in data:
            user = User(**com.pop('user'))
            self._comments.append(Comment(user=user, **com))
        return self._comments

    @property
    def crew(self):
        """All of the crew members that worked on this :class:`Movie`"""
        return [p for p in self.people if getattr(p, 'job')]

    @property
    def ids(self):
        """Accessor to the trakt, imdb, and tmdb ids, as well as the trakt.tv
        slug
        """
        return {'ids': {
            'trakt': self.trakt_id, 'slug': self.slug, 'imdb': self.imdb_id,
            'tmdb': self.tmdb_id
        }}

    @property
    def images(self):
        """All of the artwork associated with this :class:`Movie`"""
        if self._images is None:
            data = self._get_(self.images_ext)
            self._images = data.get('images')
        return self._images

    @property
    def people(self):
        """A :const:`list` of all of the :class:`People` involved in this
        :class:`Movie`, including both cast and crew
        """
        if self._people is None:
            data = self._get_(self.ext + '/people')
            crew = data.get('crew')
            cast = []
            for c in data.get('cast'):
                person = c.pop('person')
                character = c.pop('character')
                cast.append(Person(character=character, **person))

            _crew = []
            for key in crew:
                for department in crew.get(key):  # lists
                    person = department.get('person')
                    person.update({'job': department.get('job')})
                    _crew.append(Person(**person))
            self._people = cast + _crew
        return self._people

    @property
    def ratings(self):
        """Ratings (between 0 and 10) and distribution for a movie."""
        if self._ratings is None:
            self._ratings = self._get_(self.ext + '/ratings')
        return self._ratings

    @property
    def related(self):
        """The top 10 :class:`Movie`'s related to this :class:`Movie`"""
        ext = self.ext + '/related'
        data = self._get_(ext)
        movies = []
        for movie in data:
            movies.append(Movie(**movie))
        return movies

    @property
    def watching_now(self):
        """A list of all :class:`User`'s watching a movie."""
        from .users import User
        ext = self.ext + '/watching'
        data = self._get_(ext)
        users = []
        for user in data:
            users.append(User(**user))
        return users

    def add_to_library(self):
        """Add this :class:`Movie` to your library."""
        add_to_collection(self)
    add_to_collection = add_to_library

    def add_to_watchlist(self):
        """Add this :class:`Movie` to your watchlist"""
        add_to_watchlist(self)

    def comment(self, comment_body, spoiler=False, review=False):
        """Add a comment (shout or review) to this :class:`Move` on trakt."""
        comment(self, comment_body, spoiler, review)

    def dismiss(self):
        """Dismiss this movie from showing up in Movie Recommendations"""
        dismiss_recommendation(title=self.title)

    def get_releases(self, country_code='us'):
        """Returns all :class:`Release`s for a movie including country,
        certification, and release date.

        :param country_code: The 2 character country code to search from
        :return: a :const:`list` of :class:`Release` objects
        """
        ext = self.ext + '/releases/{cc}'.format(cc=country_code)
        data = self._get_(ext)
        return [Release(**release) for release in data]

    def get_translations(self, country_code='us'):
        """Returns all :class:`Translation`s for a movie, including language
        and translated values for title, tagline and overview.

        :param country_code: The 2 character country code to search from
        :return: a :const:`list` of :class:`Translation` objects
        """
        ext = self.ext + '/translations/{cc}'.format(cc=country_code)
        data = self._get_(ext)
        return [Translation(**translation) for translation in data]

    def mark_as_seen(self, watched_at=None):
        """Add this :class:`Movie`, watched outside of trakt, to your library.
        """
        add_to_history(self, watched_at)

    def mark_as_unseen(self):
        """Remove this :class:`Movie`, watched outside of trakt, from your
        library.
        """
        remove_from_history(self)

    def rate(self, rating):
        """Rate this :class:`Movie` on trakt. Depending on the current users
        settings, this may also send out social updates to facebook, twitter,
        tumblr, and path.
        """
        rate(self, rating)

    def remove_from_library(self):
        """Remove this :class:`Movie` from your library."""
        remove_from_collection(self)
    remove_from_collection = remove_from_library

    def remove_from_watchlist(self):
        remove_from_watchlist(self)

    def scrobble(self, progress, app_version, app_date):
        """Notify trakt that the current user has finished watching a movie.
        This commits this :class:`Movie` to the current users profile. You
        should use movie/watching prior to calling this method.

        :param progress: % progress, integer 0-100. It is recommended to call
            the watching API every 15 minutes, then call the scrobble API near
            the end of the movie to lock it in.
        :param app_version: Version number of the media center, be as specific
            as you can including nightly build number, etc. Used to help debug
            your plugin.
        :param app_date: Build date of the media center. Used to help debug
            your plugin.
        """
        return Scrobbler(self.to_json(), progress, app_version, app_date)

    def to_json(self):
        return {'movie': {
            'title': self.title, 'year': self.year, 'ids': self.ids
        }}

    def __str__(self):
        """String representation of a :class:`Movie`"""
        return '<Movie>: {}'.format(self.title.encode('ascii', 'ignore'))
    __repr__ = __str__
