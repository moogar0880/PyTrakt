Get Started
-----------
The main thing worth noting is how to authenticate via the trakt module. As far
as the Trakt.tv API is concerned there are two forms of authentication that you
can make. One is authenticating via your personal API Key, the other is
authenticating with your trakt.tv username and password.


Example Usage
^^^^^^^^^^^^^
Below is an example of how to specify your API Key
::

    >>> import trakt
    >>> trakt.api_key = my_api_key

For any methods that would directly interact with your user account (checking in,
getting custom recommendations, creating lists, etc...) you must authenticate with
your username and password. It is important to note that your password should be
passed in as a string, however, your raw password is never explicity stored anywhere,
only the hexdigest of it will be stored.
::

    >>> trakt.authenticate('my_username', 'my_password')

If you are worried about needing to store your password within a script that uses
this module I would recommend importing the password from an external config file or
using Python's builtin getpass module like this:
::

    >>> from getpass import getpass
    >>> trakt.authenticate('my_username', getpass('Enter Trakt.tv Password: '))
