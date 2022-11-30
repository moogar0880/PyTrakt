People
------

.. automodule:: trakt.people
    :members:
    :undoc-members:


Example Usage
^^^^^^^^^^^^^
The trakt.people module is pretty straightforward, it contains all of the tooling
for collecting information about the cast and crew of TV Shows and Movies.

To collect information about a specific person, you need only to create a
:class:`Person` instance with their name as a parameter. Like so,
::

    >>> from trakt.people import Person
    >>> heyy = Person('Matthew McConaughey')

If you don't know the person's exact name, or believe it could be obscured by
another person's name, you can also search
::

    >>> heyy = Person.search('Matthew McConaughey')[0]

Once you have your :class:`Person` instance, it's easy to collect information
about them
::

    >>> heyy.birthday
    '1969-11-04
    >>> heyy.birthplace
    'Uvalde, Texas, USA'
    >>> heyy.biography
    "Matthew David McConaughey (born November 4, 1969) is an American actor..."
    >>> heyy.images
    {'headshot': 'http://slurm.trakt.us/images/poster-dark.jpg'}

As of PyTrakt version 2.7.0, you can also access a :class:`Person`'s Movie and
television credits
::

    >>> heyy.movie_credits.crew
    {'production': [<CrewCredit> Producer - Surfer, Dude, <CrewCredit> Executive Producer - Sahara]}
    >>> heyy.movie_credits.cast
    [<ActingCredit> Man in Black - The Dark Tower,
    <ActingCredit> Arthur Brennan - The Sea of Trees,
    <ActingCredit> Beetle (voice) - Kubo and the Two Strings,
    ...
