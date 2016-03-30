PyTrakt
=======
.. image:: https://travis-ci.org/moogar0880/PyTrakt.svg
    :target: https://travis-ci.org/moogar0880/PyTrakt
    :alt: Travis CI Status

.. image:: https://landscape.io/github/moogar0880/PyTrakt/master/landscape.svg?style=flat
    :target: https://landscape.io/github/moogar0880/PyTrakt/master
    :alt: Code Health

.. image:: https://img.shields.io/pypi/dm/trakt.svg
    :target: https://pypi.python.org/pypi/trakt
    :alt: Downloads

.. image:: https://img.shields.io/pypi/l/trakt.svg
    :target: https://pypi.python.org/pypi/trakt/
    :alt: License

This module is designed to be a Pythonic interface to the `Trakt.tv <http://trakt.tv>`_.
REST API. The official documentation for which can be found `here <http://trakt.tv/api-docs/>`_.
trakt contains interfaces to all of the Trakt.tv functionality in an, ideally, easily
scriptable fashion. For more information on this module's contents and example usages
please see the `PyTrakt docs <http://pytrakt.readthedocs.org/en/latest/>`_.

More information about getting started and accessing the information you thirst for
can be found throughout the documentation below.


Installation
------------
There are two ways through which you can install trakt

Install Via Pip
^^^^^^^^^^^^^^^
To install with `pip <http://www.pip-installer.org/>`_, just run this in your terminal::

    $ pip install trakt

Get the code
^^^^^^^^^^^^
trakt is available on `GitHub <https://github.com/moogar0880/PyTrakt>`_.

You can either clone the public repository::

    $ git clone git://github.com/moogar0880/PyTrakt.git

Download the `tarball <https://github.com/moogar0880/PyTrakt/tarball/master>`_::

    $ curl -OL https://github.com/moogar0880/PyTrakt/tarball/master

Or, download the `zipball <https://github.com/moogar0880/PyTrakt/zipball/master>`_::

    $ curl -OL https://github.com/moogar0880/PyTrakt/zipball/master

Once you have a copy of the source, you can embed it in your Python package,
or install it into your site-packages easily::

    $ python setup.py install

Contributing
------------
Pull requests are graciously accepted. Any pull request should not break any tests
and should pass `flake8` style checks (unless otherwise warranted). Additionally
the user opening the Pull Request should ensure that their username and a link to
their GitHub page appears in `CONTRIBUTORS.md <https://github.com/moogar0880/PyTrakt/blob/master/CONTRIBUTORS.md>`_.


TODO
----
The following lists define the known functionality provided by the Trakt.tv API
which this module does not yet have support for. The current plan is that
support for the following features will be added over time. As always, if you
would like a feature added sooner rather than later, pull requests are most
definitely appreciated.

High Level API Features
^^^^^^^^^^^^^^^^^^^^^^^
- Pagination
- Device Authentication Workflow

Sync
^^^^
- Create a comment class to facilitate
  - returning an instance when a comment is created, instead of None
  - add ability to update and delete comments
- Add checkin support

Movies
^^^^^^
- movies/popular
- movies/played/{time_period}
- movies/watched/{time_period}
- movies/collected/{time_period}
- movies/anticipated
- movies/boxoffice
- movies/{slug}/stats

People
^^^^^^
- add credits support for movies and shows

Shows
^^^^^
- Played
- Watched
- Collected
- Anticipated
- Collection Progress
- Watched Progress
- Stats

Seasons
^^^^^^^
- extended
  - images
  - episodes
  - full
- stats

Episodes
^^^^^^^^
- stats

Users
^^^^^
- hidden everything
- likes
  - comments
  - lists
- comments
- UserList
  - items
  - comments
- history
- watchlists
  - seasons
  - episodes
