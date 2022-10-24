.. trakt documentation master file, created by
   sphinx-quickstart on Sun May 25 16:20:58 2014.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

trakt: Python interface to Trakt.tv
===================================
Release v\ |version|.

This module is designed to be a Pythonic interface to the `Trakt.tv <http://trakt.tv>`_.
REST API. The official documentation for which can be found `here <http://trakt.tv/api-docs/>`_.
trakt contains interfaces to all of the Trakt.tv functionality in an, ideally, easily
scriptable fashion.

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
trakt is available on `GitHub <https://github.com/glensc/python-pytrakt>`_.

You can either clone the public repository::

    $ git clone git://github.com/glensc/python-pytrakt.git

Download the `tarball <https://github.com/glensc/python-pytrakt/tarball/main>`_::

    $ curl -OL https://github.com/glensc/python-pytrakt/tarball/master

Or, download the `zipball <https://github.com/glensc/python-pytrakt/zipball/main>`_::

    $ curl -OL https://github.com/glensc/python-pytrakt/zipball/main

Once you have a copy of the source, you can embed it in your Python package,
or install it into your site-packages easily::

    $ python setup.py install

User Guide
----------
Below you will find links to the generated documentation of the trakt module,
including example usages.

.. toctree::
   :maxdepth: 1

   getstarted.rst
   errors.rst
   calendar.rst
   movies.rst
   people.rst
   tv.rst
   users.rst
   sync.rst
   core.rst
   sync.rst


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

