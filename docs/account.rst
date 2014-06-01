Accounts
--------

.. automodule:: trakt.account
    :members:
    :undoc-members:


Example Usage
^^^^^^^^^^^^^
This module is pretty lightweight and only contains the three basic functions
described above. You can create a new account
::

    >>> from trakt import account
    >>> account.create_account('new_username', 'new_password', 'email@email.com')


You can get a user's account settings. They are returned as a dict containing
all of a User's trakt.tv settings
::

    >>> account.settings('my_username', 'my_password')
    {'status': 'success', 'viewing': {'ratings': {'mode': 'advanced'}, 'shouts': {'show_badges': True, 'show_spoilers': False}}, 'connections': {'prowl': {'connected': False}, 'twitter': {'share_tv': True, 'share_scrobbles_end': True, 'connected': True, 'share_ratings': False, 'share_movies': True, 'share_scrobbles_start': False, 'share_checkins': False}, 'facebook': {'share_tv': True, 'share_scrobbles_end': False, 'connected': True, 'timeline_enabled': True, 'share_ratings': False, 'share_movies': True, 'share_scrobbles_start': True, 'share_checkins': False}, 'tumblr': {'share_tv': True, 'share_scrobbles_end': False, 'connected': False, 'share_ratings': False, 'share_movies': True, 'share_scrobbles_start': False, 'share_checkins': False}, 'path': {'connected': False}}, 'account': {'use_24hr': False, 'timezone': 'UM8', 'protected': False}, 'message': 'All settings for moogar0880', 'sharing_text': {'watched': 'I just watched [item]', 'watching': "I'm watching [item]"}, 'profile': {'gender': 'male', 'username': 'moogar0880', 'full_name': '', 'age': 23, 'location': 'Newmarket NH', 'about': '', 'vip': False, 'avatar': 'http://slurm.trakt.us/images/avatars/53294.1.jpg', 'last_login': 1401403481, 'url': 'http://trakt.tv/user/moogar0880', 'joined': 1342204856}}

You can also test a user's username and password. If the username and password
provided are the correct username and password, True will be returned, otherwise
False will be returned
::

    >>> account.test('my_username', 'my_password')
    True
    >>> account.test('my_username', 'a_fake_password')
    False

