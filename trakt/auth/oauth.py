from trakt.auth import get_client_info, _store


class OAuth:
    def __init__(self, username, client_id=None, client_secret=None, store=False, oauth_cb=None):
        """
        :param username: Your trakt.tv username
        :param client_id: Your Trakt OAuth Application's Client ID
        :param client_secret: Your Trakt OAuth Application's Client Secret
        :param store: Boolean flag used to determine if your trakt api auth data
            should be stored locally on the system. Default is :const:`False` for
            the security conscious
        :param oauth_cb: Callback function to handle the retrieving of the OAuth
            PIN. Default function `_terminal_oauth_pin` for terminal auth
        """
        self.username = username
        self.client_id = client_id
        self.client_secret = client_secret
        self.store = store
        self.oauth_cb = self.terminal_oauth_pin if oauth_cb is None else oauth_cb

    def authenticate(self):
        """Generate an access_token to allow your application to authenticate via
        OAuth

        :return: Your OAuth access token
        """
        global CLIENT_ID, CLIENT_SECRET, OAUTH_TOKEN
        if self.client_id is None and self.client_secret is None:
            self.client_id, self.client_secret = get_client_info()
        CLIENT_ID, CLIENT_SECRET = self.client_id, self.client_secret
        HEADERS['trakt-api-key'] = CLIENT_ID

        authorization_base_url = urljoin(BASE_URL, '/oauth/authorize')
        token_url = urljoin(BASE_URL, '/oauth/token')

        # OAuth endpoints given in the API documentation
        oauth = OAuth2Session(CLIENT_ID, redirect_uri=REDIRECT_URI, state=None)

        # Authorization URL to redirect user to Trakt for authorization
        authorization_url, _ = oauth.authorization_url(authorization_base_url, username=self.username)

        # Calling callback function to get the OAuth PIN
        oauth_pin = self.oauth_cb(authorization_url)

        # Fetch, assign, and return the access token
        oauth.fetch_token(token_url, client_secret=CLIENT_SECRET, code=oauth_pin)
        OAUTH_TOKEN = oauth.token['access_token']
        OAUTH_REFRESH = oauth.token['refresh_token']
        OAUTH_EXPIRES_AT = oauth.token["created_at"] + oauth.token["expires_in"]

        if self.store:
            _store(CLIENT_ID=CLIENT_ID, CLIENT_SECRET=CLIENT_SECRET,
                   OAUTH_TOKEN=OAUTH_TOKEN, OAUTH_REFRESH=OAUTH_REFRESH,
                   OAUTH_EXPIRES_AT=OAUTH_EXPIRES_AT)
        return OAUTH_TOKEN

    @staticmethod
    def terminal_oauth_pin(authorization_url):
        """Default OAuth callback used for terminal applications.

        :param authorization_url: Predefined url by function `oauth_auth`. URL will
            be prompted to you in the terminal
        :return: OAuth PIN
        """
        print('Please go here and authorize,', authorization_url)

        # Get the authorization verifier code from the callback url
        response = input('Paste the Code returned here: ')
        return response
