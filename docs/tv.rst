Television
----------

.. automodule:: trakt.tv
    :members:
    :undoc-members:


Example Usage
^^^^^^^^^^^^^
The trakt.tv module has interfaces to all of the TV resources mentioned above and
is almost a direct port of the trakt.movies module. It has the same interfaces to
dismiss shows from recommendations, getting recommendations, rating a list of shows,
rating a list of episodes, getting a list of valid show genres, a list of trending
shows, and getting a list of recently updated shows and dealing with specific
shows, seasons, and episodes.

For our first example let's start by grabbing a specific show
::

    >>> from trakt.tv import TVShow
    >>> it_crowd = TVShow('The IT Crowd')

Well that was pretty painless. Ok, now let's pull some data out of our ``it_crowd``
object
::

    >>> it_crowd.people
    [<Person>: Chris O'Dowd, <Person>: Katherine Parkinson, <Person>: None,
    <Person>: Richard Ayoade, <Person>: Chris Morris, <Person>: Matt Berry, <Person>: Noel Fielding]
    >>> it_crowd.top_episodes
    [<TVEpisode>: The IT Crowd S1E1 Yesterday's Jam, <TVEpisode>: The IT Crowd S1E2 Calamity Jen,
     <TVEpisode>: The IT Crowd S2E1 The Work Outing, <TVEpisode>: The IT Crowd S1E4 The Red Door,...
    >>> it_crowd.top_watchers
    [<User>: 'Vaelek', <User>: 'Governa', <User>: 'shanos404', <User>: 'b_jammin666',
    <User>: 'pavvoc', <User>: 'heartbraden', <User>: 'tressal', <User>: 'hherrera',...
    >>> it_crowd.genres
    [Genre(name='Comedy', slug='comedy')]

Now that we've gotten some information on the show, let's start doing something
interesting and interacting with the API via the :class:`TVShow`'s methods
::

    >>> it_crowd.add_to_library()
    >>> it_crowd.comment('Wow, I REALLY love this show')
    >>> it_crowd.comment('They should never have given Jen the internet.',
                         spoiler=True, review=True)

Now that we've gotten some information on the show, let's dive down and get some
information on the show's seasons and episodes
::

    >>> s1 = it_crowd.seasons[1]
    >>> s1.episodes
    [<TVEpisode>: The IT Crowd S1E-1 Yesterday's Jam, <TVEpisode>: The IT Crowd S1E-1 Calamity Jen,
    <TVEpisode>: The IT Crowd S1E-1 Fifty-Fifty, <TVEpisode>: The IT Crowd S1E-1 The Red Door,
    <TVEpisode>: The IT Crowd S1E-1 The Haunting of Bill Crouse, <TVEpisode>: The IT Crowd S1E-1 Aunt Irma Visits]
    >>> pilot = s1.episodes[0]
    >>> pilot.title
    "Yesterday's Jam"
    >>> pilot.overview
    'Jen is hired as the manager Reynholm Industries although she doesn't know the first thing about computers.'

