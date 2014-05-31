trakt.users
-----------

.. autoclass:: trakt.users.User(username)
    :members:
    :undoc-members:

.. autoclass:: trakt.users.UserList(user_name, slug='')
    :members:
    :undoc-members:

Examples
^^^^^^^^
To access a :class:`User` all you need do is pass the :class:`User`'s username
to the :class:`User`'s __init__ method
::

    >>> from trakt.users import User
    >>> my = User('moogar0880')
    >>> my
    '<User>: moogar0880'

Good, now we have a hold of the :class:`User` object. Now we can get all of the information
available from this trakt.tv :class:`User`.
::

    >>> my.gender
    'male'
    >>> my.location
    'Newmarket NH'
    >>> my.movie_collection
    [<Movie>: b'2 Fast 2 Furious', <Movie>: b'A Beautiful Mind', <Movie>: b'A Bronx Tale', <Movie>: b"A Bug's Life", <Movie>: b'A Christmas Carol',...


