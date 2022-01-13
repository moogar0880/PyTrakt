def pin_auth(pin=None, client_id=None, client_secret=None, store=False):
    """Generate an access_token from a Trakt API PIN code.

    :param pin: Optional Trakt API PIN code. If one is not specified, you will
        be prompted to go generate one
    :param client_id: The oauth client_id for authenticating to the trakt API.
    :param client_secret: The oauth client_secret for authenticating to the
        trakt API.
    :param store: Boolean flag used to determine if your trakt api auth data
        should be stored locally on the system. Default is :const:`False` for
        the security conscious
    :return: Your OAuth access token
    """
    global OAUTH_TOKEN, CLIENT_ID, CLIENT_SECRET
    CLIENT_ID, CLIENT_SECRET = client_id, client_secret
    if client_id is None and client_secret is None:
        CLIENT_ID, CLIENT_SECRET = _get_client_info(app_id=True)
    if pin is None and APPLICATION_ID is None:
        print('You must set the APPLICATION_ID of the Trakt application you '
              'wish to use. You can find this ID by visiting the following '
              'URL.')
        print('https://trakt.tv/oauth/applications')
        sys.exit(1)
    if pin is None:
        print('If you do not have a Trakt.tv PIN, please visit the following '
              'url and log in to generate one.')
        pin_url = 'https://trakt.tv/pin/{id}'.format(id=APPLICATION_ID)
        print(pin_url)
        pin = input('Please enter your PIN: ')
    args = {'code': pin,
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
