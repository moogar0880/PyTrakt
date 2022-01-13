def device_auth(client_id=None, client_secret=None, store=False):
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

    :param client_id: Your Trakt OAuth Application's Client ID
    :param client_secret: Your Trakt OAuth Application's Client Secret
    :param store: Boolean flag used to determine if your trakt api auth data
        should be stored locally on the system. Default is :const:`False` for
        the security conscious
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

    response = get_device_code(client_id=client_id,
                               client_secret=client_secret)
    device_code = response['device_code']
    interval = response['interval']

    # No need to check for expiration, the API will notify us.
    while True:
        response = get_device_token(device_code, client_id, client_secret,
                                    store)

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
