trakt.movies
------------

.. automodule:: trakt.movies
    :members:
    :undoc-members:


Example Usage
^^^^^^^^^^^^^
The trakt.movies module has a handful of functionality for interfacing with
the Movies hosted on Trakt.tv. The module has a few functions which you will
need to be authenticated for. The :func:`dismiss_recommendation` function will
block the specified movie from being shown in your recommended movies.
::

    >>> from trakt.movies import dismiss_recommendation
    >>> dismiss_recommendation(imdb_id='tt3139072', title='Son of Batman',
    ...                        year=2014)


This code snippet would prevent Son of Batman from appearing in your recommended
movies list. Following the previous example you can use the
:func:`get_recommended_movies` function to get the list of movies recommended for
the currently authenticated user.
::

    >>> from trakt.movies import get_recommended_movies
    >>> all_movies = get_recommended_movies()
    >>> all_movies
    [<Movie>: b'The Dark Knight', <Movie>: b'WALLE', <Movie>: b'Up', <Movie>: b'Toy Story',...


There's also a function to quickly rate a list of movies as the currently
authenticated user.
::

    >>> from trakt.movies import Movie, rate_movies
    >>> rate_movies(all_movies, 'love')

There are a few properties that belong to the trakt.movies module as well.
::

    >>> from trakt import movies
    >>> movies.genres
    [Genre(name='Action', slug='action'), Genre(name='Adventure', slug='adventure'),...
    >>> movies.trending_movies
    [<Movie>: b'The LEGO Movie', <Movie>: b'Non-Stop', <Movie>: b'Frozen', <Movie>: b'RoboCop',...
    >>> movies.updated_movies()
    []

Now to the Movie object. It's pretty straightforward, you provide a title and an
optional year, and you will be returned an interface to that Movie on trakt.tv.
::

    >>> from trakt.movies import Movie
    >>> batman = Movie('Son of Batman')
    >>> batman.overview
    'Batman learns that he has a violent, unruly pre-teen son with Talia al Ghul named Damian Wayne who is secretly being...
    >>> batman.released_iso
    '2014-04-20T07:00:00'
    >>> batman.genres
    [Genre(name='Action', slug='action'), Genre(name='Adventure', slug='adventure'), Genre(name='Animation', slug='animation')]
    >>> batman.add_to_library()
    >>> batman.mark_as_seen()



