Get Started
-----------
The main thing worth noting is how to authenticate via the trakt module. As of
Trakt2.0, you need to generate an authentication token (API Key) in order to use
this application. Regardless of whether you are a single user or a media center
you'll want to hold on to this key for as long as it's good for. To generate this
key you can interactively run PyTrakt's `init` function like detailed below:


Example Usage
^^^^^^^^^^^^^
The simplest way to generate an API key is to let `trakt.init` walk you through
the process of generating one from scratch. Currently PyTrakt supports both OAuth
and PIN auth methods (the default is PIN).

PIN Auth
^^^^^^^^
You can authenticate to trakt via PIN Auth like so,

::

    >>> import trakt
    >>> trakt.APPLICATION_ID = 'MY_APPLICATION_ID'
    >>> # to get an id for your app, visit https://trakt.tv/oauth/applications
    >>> trakt.init()
    If you do not have a Trakt.tv PIN, please visit the following url and log in to generate one.
    https://trakt.tv/pin/MY_APPLICATION_ID
    Please enter your PIN:
    >>> # Once you've pasted your PIN, you'll be completely authenticated and
    >>> # ready to use PyTrakt

If you already have a Trakt PIN generated, you can provide it to the `init` function

::

    >>> from trakt import init
    >>> init('MY_PIN')

And you're all set

OAuth Auth
^^^^^^^^^^
You can also initialize using OAuth authentication like so,

::

    >>> from trakt import init
    >>> trakt.AUTH_METHOD = trakt.OAUTH_AUTH  # Set the auth method to OAuth
    >>> init('myusername')
    If you do not have a client ID and secret. Please visit the following url to create them.
    http://trakt.tv/oauth/applications
    Please enter your client id:
    Please enter your client secret:

    Please go here and authorize, <authorization_url>
    Paste the Code returned here:
    >>> # paste your code above and your access token will be returned

This example assumes that you haven't already created an OAuth application on Trakt
yet. As of PyTrakt v2.0.0, if you have already registered your OAuth application
on Trakt, you can specify your CLIENT_ID and CLIENT_SECRET to the `init` function
and skip the first couple steps, like so
::

    >>> from trakt import init
    >>> init('myusername', client_id=my_client_id, client_secret=my_client_secret)
    Please go here and authorize, <authorization_url>
    Paste the Code returned here:
    >>> # paste your code above and your access token will be returned

As of PyTrakt v2.0.0, `trakt.init` also exposes a `store` flag. This boolean
flag can be used to store your PyTrakt API authentication data at the configurable
`trakt.core.CONFIG_PATH` (the default is ~/.pytrakt.json). This will allow PyTrakt
to dynamically load in your authorization settings when it runs, so that you won't
have to worry about including that setup in your utilities. The store flag is
set to `False` by default to appease those of you out there who are more security
conscious. To set the `store` flag you can simply run `init` like so
::

    >>> from trakt import init
    >>> init('myusername', store=True)


Should you choose to store your credentials in another way and not to set the
`store` flag, you will need to ensure that your application applies the
following settings before attempting to interact with Trakt

* `trakt.core.api_key`
* `trakt.core.CLIENT_ID`
* `trakt.core.CLIENT_SECRET`

These can be set like so
::

    >>> import trakt
    >>> trakt.core.api_key = my_api_key
    >>> trakt.core.CLIENT_ID = my_client_id
    >>> trakt.core.CLIENT_SECRET = my_client_secret

This is all of the authentication you'll need to perform to use the latest version
of Trakt's API
