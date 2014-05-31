trakt.people
------------

.. automodule:: trakt.people
    :members:
    :undoc-members:


Example Usage
^^^^^^^^^^^^^
The trakt.people module is straightforward, it contains only one class, the
:class:`Person` class.
::

    >>> from trakt.people import Person
    >>> heyy = Person('Matthew McConaughey')
    >>> heyy.birthday
    '1969-11-04
    >>> heyy.birthplace
    'Uvalde, Texas, USA'
    >>> heyy.biography
    '\u200bFrom Wikipedia, the free encyclopedia. \xa0\n\nMatthew David McConaughey (born November 4, 1969) is an American actor.\n...'
    >>> heyy.images
    {'headshot': 'http://slurm.trakt.us/images/poster-dark.jpg'}

