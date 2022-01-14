import sys

from trakt.api import HttpClient
from trakt.auth import get_client_info
from trakt.config import AuthConfig


class PinAuthAdapter:
    #: The OAuth2 Redirect URI for your OAuth Application
    REDIRECT_URI: str = 'urn:ietf:wg:oauth:2.0:oob'

    def __init__(self, client: HttpClient, config: AuthConfig, pin=None, client_id=None, client_secret=None):
        """
        :param pin: Optional Trakt API PIN code. If one is not specified, you will
            be prompted to go generate one
        :param client_id: The oauth client_id for authenticating to the trakt API.
        :param client_secret: The oauth client_secret for authenticating to the
            trakt API.
        """
        self.pin = pin
        self.client = client
        self.config = config
        self.client_id = client_id
        self.client_secret = client_secret

    def authenticate(self):
        """Generate an access_token from a Trakt API PIN code.

        :return: Your OAuth access token
        """

        self.update_tokens()

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
        data = {
            'code': self.pin,
            'redirect_uri': self.REDIRECT_URI,
            'grant_type': 'authorization_code',
            'client_id': self.config.CLIENT_ID,
            'client_secret': self.config.CLIENT_SECRET,
        }

        response = self.client.post('/oauth/token', data)
        self.config.OAUTH_TOKEN = response.get('access_token', None)

        # self.config.update(
        #     CLIENT_ID=CLIENT_ID,
        #     CLIENT_SECRET=CLIENT_SECRET,
        #     OAUTH_TOKEN=OAUTH_TOKEN,
        #     APPLICATION_ID=APPLICATION_ID
        # )

        return self.config.OAUTH_TOKEN

    def update_tokens(self):
        """
        Update client_id, client_secret from input or ask them interactively
        """
        if self.client_id is None and self.client_secret is None:
            self.client_id, self.client_secret = get_client_info()
        self.config.CLIENT_ID, self.config.CLIENT_SECRET = self.client_id, self.client_secret
