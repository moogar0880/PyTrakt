Get Started
-----------
The main thing worth noting is how to authenticate via the trakt module. As of
Trakt2.0, you need to generate an authentication token (API Key) in order to use
this application. Regardless of whether you are a single user or a media center
you'll want to hold on to this key for as long as it's good for. To generate this
key you can interactively run PyTrakt's init function like detailed below:


Example Usage
^^^^^^^^^^^^^
To generate an API key simply run
::

    >>> from trakt import init
    >>> init('myusername')
    Please go here and authorize, <authorization_url>
    Paste the Code returned here:
    >>> # paste your code above and your access token will be returned

Once you have your API key all that's nessecary to do is to assign it to `trakt.api_key`
like describted below

Below is an example of how to specify your API Key
::

    >>> import trakt
    >>> trakt.api_key = my_api_key

This is all of the authentication you'll need to perform to use the latest version
of Trakt's API

