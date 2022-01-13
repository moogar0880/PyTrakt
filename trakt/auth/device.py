import time

from trakt.auth import get_client_info


class DeviceAuth:
    def __init__(self, client_id=None, client_secret=None, store=False):
        """
        :param client_id: Your Trakt OAuth Application's Client ID
        :param client_secret: Your Trakt OAuth Application's Client Secret
        :param store: Boolean flag used to determine if your trakt api auth data
            should be stored locally on the system. Default is :const:`False` for
            the security conscious
        """
        self.client_id = client_id
        self.client_secret = client_secret
        self.store = store

    def authenticate(self):
        """Process for authenticating using device authentication.

        The function will attempt getting the device_id, and provide
        the user with a url and code. After getting the device
        id, a timer is started to poll periodic for a successful authentication.
        This is a blocking action, meaning you
        will not be able to run any other code, while waiting for an access token.

        If you want more control over the authentication flow, use the functions
        get_device_code and get_device_token.
        Where poll_for_device_token will check if the "offline"
        authentication was successful.

        :return: A dict with the authentication result.
        Or False of authentication failed.
        """
        error_messages = {
            404: 'Invalid device_code',
            409: 'You already approved this code',
            410: 'The tokens have expired, restart the process',
            418: 'You explicitly denied this code',
        }

        success_message = (
            "You've been successfully authenticated. "
            "With access_token {access_token} and refresh_token {refresh_token}"
        )

        response = self.get_device_code(client_id=self.client_id, client_secret=self.client_secret)
        device_code = response['device_code']
        interval = response['interval']

        # No need to check for expiration, the API will notify us.
        while True:
            response = self.get_device_token(device_code, self.client_id, self.client_secret, self.store)

            if response.status_code == 200:
                print(success_message.format_map(response.json()))
                break

            elif response.status_code == 429:  # slow down
                interval *= 2

            elif response.status_code != 400:  # not pending
                print(error_messages.get(response.status_code, response.reason))
                break

            time.sleep(interval)

        return response

    def get_device_code(self, client_id=None, client_secret=None):
        """Generate a device code, used for device oauth authentication.

        Trakt docs: https://trakt.docs.apiary.io/#reference/
        authentication-devices/device-code
        :param client_id: Your Trakt OAuth Application's Client ID
        :param client_secret: Your Trakt OAuth Application's Client Secret
        :return: Your OAuth device code.
        """
        global CLIENT_ID, CLIENT_SECRET, OAUTH_TOKEN
        if client_id is None and client_secret is None:
            client_id, client_secret = get_client_info()
        CLIENT_ID, CLIENT_SECRET = client_id, client_secret
        HEADERS['trakt-api-key'] = CLIENT_ID

        device_code_url = urljoin(BASE_URL, '/oauth/device/code')
        headers = {'Content-Type': 'application/json'}
        data = {"client_id": CLIENT_ID}

        device_response = session.post(device_code_url,
                                       json=data, headers=headers).json()
        print('Your user code is: {user_code}, please navigate to '
              '{verification_url} to authenticate'.format(
            user_code=device_response.get('user_code'),
            verification_url=device_response.get('verification_url')
        ))

        device_response['requested'] = time.time()
        return device_response

    def get_device_token(self, device_code, client_id=None, client_secret=None,
                         store=False):
        """
        Trakt docs: https://trakt.docs.apiary.io/#reference/
        authentication-devices/get-token
        Response:
        {
          "access_token": "",
          "token_type": "bearer",
          "expires_in": 7776000,
          "refresh_token": "",
          "scope": "public",
          "created_at": 1519329051
        }
        :return: Information regarding the authentication polling.
        :return type: dict
        """
        global CLIENT_ID, CLIENT_SECRET, OAUTH_TOKEN, OAUTH_REFRESH
        if client_id is None and client_secret is None:
            client_id, client_secret = get_client_info()
        CLIENT_ID, CLIENT_SECRET = client_id, client_secret
        HEADERS['trakt-api-key'] = CLIENT_ID

        data = {
            "code": device_code,
            "client_id": CLIENT_ID,
            "client_secret": CLIENT_SECRET
        }

        response = session.post(
            urljoin(BASE_URL, '/oauth/device/token'), json=data
        )

        # We only get json on success.
        if response.status_code == 200:
            data = response.json()
            OAUTH_TOKEN = data.get('access_token')
            OAUTH_REFRESH = data.get('refresh_token')
            OAUTH_EXPIRES_AT = data.get("created_at") + data.get("expires_in")

            if store:
                _store(
                    CLIENT_ID=CLIENT_ID, CLIENT_SECRET=CLIENT_SECRET,
                    OAUTH_TOKEN=OAUTH_TOKEN, OAUTH_REFRESH=OAUTH_REFRESH,
                    OAUTH_EXPIRES_AT=OAUTH_EXPIRES_AT
                )

        return response
