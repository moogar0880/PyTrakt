def oauth_auth(username, client_id=None, client_secret=None, store=False,
               oauth_cb=_terminal_oauth_pin):
    """Generate an access_token to allow your application to authenticate via
    OAuth

    :param username: Your trakt.tv username
    :param client_id: Your Trakt OAuth Application's Client ID
    :param client_secret: Your Trakt OAuth Application's Client Secret
    :param store: Boolean flag used to determine if your trakt api auth data
        should be stored locally on the system. Default is :const:`False` for
        the security conscious
    :param oauth_cb: Callback function to handle the retrieving of the OAuth
        PIN. Default function `_terminal_oauth_pin` for terminal auth
    :return: Your OAuth access token
    """
    global CLIENT_ID, CLIENT_SECRET, OAUTH_TOKEN
    if client_id is None and client_secret is None:
        client_id, client_secret = _get_client_info()
    CLIENT_ID, CLIENT_SECRET = client_id, client_secret
    HEADERS['trakt-api-key'] = CLIENT_ID

    authorization_base_url = urljoin(BASE_URL, '/oauth/authorize')
    token_url = urljoin(BASE_URL, '/oauth/token')

    # OAuth endpoints given in the API documentation
    oauth = OAuth2Session(CLIENT_ID, redirect_uri=REDIRECT_URI, state=None)

    # Authorization URL to redirect user to Trakt for authorization
    authorization_url, _ = oauth.authorization_url(authorization_base_url,
                                                   username=username)

    # Calling callback function to get the OAuth PIN
    oauth_pin = oauth_cb(authorization_url)

    # Fetch, assign, and return the access token
    oauth.fetch_token(token_url, client_secret=CLIENT_SECRET, code=oauth_pin)
    OAUTH_TOKEN = oauth.token['access_token']
    OAUTH_REFRESH = oauth.token['refresh_token']
    OAUTH_EXPIRES_AT = oauth.token["created_at"] + oauth.token["expires_in"]

    if store:
        _store(CLIENT_ID=CLIENT_ID, CLIENT_SECRET=CLIENT_SECRET,
               OAUTH_TOKEN=OAUTH_TOKEN, OAUTH_REFRESH=OAUTH_REFRESH,
               OAUTH_EXPIRES_AT=OAUTH_EXPIRES_AT)
    return OAUTH_TOKEN
