class PinAuth:
    def __init__(self, pin=None, client_id=None, client_secret=None, store=False):
        """
        :param pin: Optional Trakt API PIN code. If one is not specified, you will
            be prompted to go generate one
        :param client_id: The oauth client_id for authenticating to the trakt API.
        :param client_secret: The oauth client_secret for authenticating to the
            trakt API.
        :param store: Boolean flag used to determine if your trakt api auth data
            should be stored locally on the system. Default is :const:`False` for
            the security conscious
        """
        self.pin = pin
        self.client_id = client_id
        self.client_secret = client_secret
        self.store = store

    def authenticate(self):
        """Generate an access_token from a Trakt API PIN code.

        :return: Your OAuth access token
        """

        global OAUTH_TOKEN, CLIENT_ID, CLIENT_SECRET
        CLIENT_ID, CLIENT_SECRET = self.client_id, self.client_secret
        if self.client_id is None and self.client_secret is None:
            CLIENT_ID, CLIENT_SECRET = _get_client_info(app_id=True)
        if self.pin is None and APPLICATION_ID is None:
            print('You must set the APPLICATION_ID of the Trakt application you '
                  'wish to use. You can find this ID by visiting the following '
                  'URL.')
            print('https://trakt.tv/oauth/applications')
            sys.exit(1)
        if self.pin is None:
            print('If you do not have a Trakt.tv PIN, please visit the following '
                  'url and log in to generate one.')
            pin_url = 'https://trakt.tv/pin/{id}'.format(id=APPLICATION_ID)
            print(pin_url)
            self.pin = input('Please enter your PIN: ')
        args = {'code': self.pin,
                'redirect_uri': REDIRECT_URI,
                'grant_type': 'authorization_code',
                'client_id': CLIENT_ID,
                'client_secret': CLIENT_SECRET}

        response = session.post(''.join([BASE_URL, '/oauth/token']), data=args)
        OAUTH_TOKEN = response.json().get('access_token', None)

        if store:
            _store(CLIENT_ID=CLIENT_ID, CLIENT_SECRET=CLIENT_SECRET,
                   OAUTH_TOKEN=OAUTH_TOKEN, APPLICATION_ID=APPLICATION_ID)
        return OAUTH_TOKEN
