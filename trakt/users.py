"""Interfaces to all of the User objects offered by the Trakt.tv API"""
from collections import namedtuple

from . import BaseAPI
from .tv import TVShow, TVSeason, TVEpisode
from .movies import Movie
from .calendar import UserCalendar
import trakt
__author__ = 'Jon Nappi'
__all__ = ['User', 'UserList']


Request = namedtuple('Request', ['username', 'protected', 'full_name',
                                 'requested', 'vip', 'url', 'avatar', 'joined',
                                 'about', 'location', 'age', 'gender'])


def approve_request(user_name, follow_back=False):
    """Approve a follower request from *user_name* if one exists"""
    ext = 'network/approve/{}'.format(trakt.api_key)
    args = {'user': user_name, 'follow_back': follow_back}
    BaseAPI()._post_(ext, args)


def deny_request(user_name):
    """Deny a follower request from *user_name* if one exists"""
    ext = 'network/deny/{}'.format(trakt.api_key)
    args = {'user': user_name}
    BaseAPI()._post_(ext, args)


def follow(user_name):
    """Follow a user with *user_name*. If the user has a protected profile, the
    follow request will be in a pending state. If they have a public profile,
    they will be followed immediately.
    """
    ext = 'network/follow/{}'.format(trakt.api_key)
    args = {'user': user_name}
    BaseAPI()._post_(ext, args)


def unfollow(user_name):
    """Unfollow a user you're currently following with a username of *user_name*
    """
    ext = 'network/unfollow/{}'.format(trakt.api_key)
    args = {'user': user_name}
    BaseAPI()._post_(ext, args)


def get_all_requests():
    """Get a list of all follower requests including the timestamp when the
    request was made. Use the approve and deny methods to manage each request.
    """
    ext = 'network/requests/{}'.format(trakt.api_key)
    data = BaseAPI()._post_(ext)
    request_list = []
    for request in data:
        request_list.append(Request(**request))
    return request_list


class UserList(BaseAPI):
    """A list created by a Trakt.tv :class:`User`"""
    def __init__(self, user_name, name=None, slug=None, description=None,
                 privacy='private', show_numbers=True, allow_shouts=True,
                 **kwargs):
        super(UserList, self).__init__()
        self.username = user_name
        self._name = name
        self._description = description
        self._privacy = privacy
        self._show_numbers = show_numbers
        self._allow_shouts = allow_shouts
        self.slug = slug
        self.url = None
        self.items = []
        # If there was no slug passed in but there was a name, we know we're
        # creating a new UserList
        if slug is None and name is not None:
            ext = 'lists/add/{}'.format(trakt.api_key)
            args = {'name': self._name, 'description': self._description,
                    'privacy': self._privacy, 'show_numbers': self._show_numbers,
                    'allow_shouts': self._allow_shouts}
            real_args = {x: args[x] for x in args if args[x] is not None}
            response = self._post_(ext, real_args)
            self._build(response)
        elif len(kwargs) > 0:
            self._build(kwargs)
        else:
            self._search(self.slug or self._name.lower().replace(' ', '-'))

    def _build(self, data):
        """Build this object from the fields in *data*"""
        private = ('name', 'description', 'privacy', 'show_numbers',
                   'allow_shouts')
        for key, val in data.items():
            if key in private:
                setattr(self, '_' + key, val)
            else:
                setattr(self, key, val)

    def _search(self, slug):
        """Search for an existing UserList"""
        ext = '/user/list.json/{}/{}/{}'.format(trakt.api_key, self.username,
                                                slug)
        data = self._get_(ext)
        for key, val in data.items():
            if key != 'items':
                setattr(self, key, val)
            else:
                self.items = []
                for item in val:
                    item_type = item.get('type')
                    for item_key, item_val in item.items():
                        if item_type == 'movie':
                            movie_data = item_val['movie']
                            title = movie_data.get('title', None)
                            self.items.append(Movie(title, **movie_data))
                        elif item_type == 'show':
                            show_data = item_val['show']
                            title = show_data.get('title', None)
                            self.items.append(TVShow(title, **show_data))

    def add_items(self, items):
        """Add *items* to this :class:`UserList`, where items is an iterable"""
        items_list = []
        trakt_types = (TVShow, TVSeason, TVEpisode, Movie)
        for item in items:
            if isinstance(item, dict):
                items_list.append(item)
            elif isinstance(item, trakt_types):
                self.items.append(item)
                items_list.append(item._list_json)
        ext = 'lists/items/add/{}'.format(trakt.api_key)
        args = {'slug': self.slug, 'items': items_list}
        self._post_(ext, args)

    def remove_items(self, items):
        """Remove *items* to this :class:`UserList`, where items is an iterable
        """
        items_list = []
        trakt_types = (TVShow, TVSeason, TVEpisode, Movie)
        for item in items:
            if isinstance(item, dict):
                items_list.append(item)
            elif isinstance(item, trakt_types):
                self.items.append(item)
                items_list.append(item._list_json)
        ext = 'lists/items/delete/{}'.format(trakt.api_key)
        args = {'slug': self.slug, 'items': items_list}
        self._post_(ext, args)

    def __property_update(self, key, val):
        """Update an attribute of this :class:`UserList`"""
        ext = 'lists/update/{}'.format(trakt.api_key)
        args = {'slug': self.slug, key: val}
        self._post_(ext, args)
        setattr(self, key, val)

    def __len__(self):
        """Return the length of this :class:`UserList`"""
        return len(self.items)

    @property
    def name(self):
        """The list name. This must be unique across the Trakt.tv system."""
        return self._name
    @name.setter
    def name(self, value):
        self.__property_update('name', value)

    @property
    def description(self):
        """Optional but recommended description of what the list contains."""
        return self._description
    @description.setter
    def description(self, value):
        self.__property_update('description', value)

    @property
    def privacy(self):
        """Privacy level of this :class:`UserList` must be one of private,
        friends, or public.
        """
        return self._privacy
    @privacy.setter
    def privacy(self, value):
        valid = ('private', 'friends', 'public')
        if value in valid:
            self.__property_update('privacy', value)

    @property
    def show_numbers(self):
        """A boolean flag to determine if this  :class:`UserList` should show
        numbers for each item. This is useful for ranked lists. Must be True or
        False
        """
        return self._show_numbers
    @show_numbers.setter
    def show_numbers(self, value):
        if isinstance(value, bool):
            self.__property_update('show_numbers', value)

    @property
    def allow_shouts(self):
        """A boolean flag to determine if this :class:`UserList` allows
        discussion by users who have access. Must be True or False
        """
        return self._allow_shouts
    @allow_shouts.setter
    def allow_shouts(self, value):
        if isinstance(value, bool):
            self.__property_update('allow_shouts', value)

    def delete(self):
        """Delete this :class:`UserList`"""
        ext = 'lists/delete/{}'.format(trakt.api_key)
        url = self.base_url + ext
        args = {'slug': self.slug}
        self._post_(url, args)


class User(BaseAPI):
    """A Trakt.tv User"""
    def __init__(self, username, **kwargs):
        super(User, self).__init__()
        self.username = username
        self._calendar = self._last_activity = self._watching = None
        self._movies = self._movie_collection = self._movies_watched = None
        self._shows = self._show_collection = self._shows_watched = None
        self._lists = self._followers = self._following = self._friends = None
        self._collected = self._watched = self._episode_ratings = None
        self._show_ratings = self._movie_ratings = None
        self._episode_watchlist = self._show_watchlist = None
        self._movie_watchlist = None
        if len(kwargs) > 0:
            for key, val in kwargs.items():
                setattr(self, key, val)
        else:
            ext = 'user/profile.json/{}/{}'.format(trakt.api_key, self.username)
            data = self._get_(ext)
            for key, val in data.items():
                if key == 'watched':
                    pass
                else:
                    setattr(self, '_' + key, val)

    def follow(self):
        """Follow this :class:`User`"""
        follow(self.username)

    def unfollow(self):
        """Unfollow this :class:`User` if you already follow them"""
        unfollow(self.username)

    def get_calendar(self, date=None, days=None):
        """Get this :class:`User`'s :class:`UserCalendar` for the specified date
        range.
        """
        self._calendar = UserCalendar(self.username, date=date, days=days)
        return self._calendar

    def get_list(self, title):
        """Get the specified list from this :class:`User`. Protected
        :class:`User`'s won't return any data unless you are friends. To view
        your own private lists, you will need to authenticate as yourself.
        """
        return UserList(self.username, title)

    @property
    def calendar(self):
        """A :class:`UserCalendar` of this :class:`Users` shows that are airing
        during the next 7 days. Protected users won't return any data
        unless you are friends.
        """
        if self._calendar is None:
            self._calendar = UserCalendar(self.username)
        return self._calendar

    @property
    def last_activity(self):
        """The last timestamp of certain activities on this :class:`User`'s
        account. This is useful with syncing since timestamps are set for both
        actions and unactions (i.e. seen and unseen). For example, run this API
        on a regular basis and cache the timestamp. If the timestamp is newer
        than what you have cached, sync up the changes for that section."""
        if self._last_activity is None:
            ext = 'user/lastactivity.json/{}/{}'.format(trakt.api_key,
                                                        self.username)
            data = self._get_(ext)
            self._last_activity = data
        return self._last_activity

    @property
    def watching(self):
        """The :class:`TVEpisode` or :class:`Movie` this :class:`User` is
        currently watching. If they aren't watching anything, a blank object
        will be returned. Protected users won't return any data unless you are
        friends.
        """
        ext = 'user/watching.json/{}/{}'.format(trakt.api_key, self.username)
        data = self._get_(ext)
        if len(data) > 0:
            media_type = data.get('type')
            if media_type == 'movie':
                pass
            elif media_type == 'episode':
                pass

        return self._watching

    def __movie_list(self, url):
        """Return a list of :class:`Movie` objects returned from the provided
        url extension
        """
        data = self._get_(url)
        to_ret = []
        if len(data) > 0:
            for movie_data in data:
                to_ret.append(Movie(**movie_data))
        return to_ret

    def __str__(self):
        """String representation of a :class:`User`"""
        return '<User>: {}'.format(self.username.encode('ascii', 'ignore'))
    __repr__ = __str__

    @property
    def movies(self):
        """All :class:`Movie`'s in this :class:`User`'s library. Each movie will
        indicate if it's in this :class:`User`'s collection and how many plays
        it has. Protected :class:`User`'s won't return any data unless you are
        friends.
        """
        ext = 'user/library/movies/all.json/{}/{}'.format(trakt.api_key,
                                                          self.username)
        self._movies = self.__movie_list(ext)
        return self._movies

    @property
    def movie_collection(self):
        """All :class:`Movie`'s in this :class:`User`'s library collection.
        Collection items might include blu-rays, dvds, and digital downloads.
        Protected users won't return any data unless you are friends.
        """
        ext = 'user/library/movies/collection.json/{}/{}'.format(trakt.api_key,
                                                                 self.username)
        self._movie_collection = self.__movie_list(ext)
        return self._movie_collection

    @property
    def movies_watched(self):
        """All :class:`Movie`'s in this :class:`User`'s library collection.
        Collection items might include blu-rays, dvds, and digital downloads.
        Protected users won't return any data unless you are friends.
        """
        ext = '/user/library/movies/watched.json/{}/{}'.format(trakt.api_key,
                                                               self.username)
        url = self.base_url + ext
        self._movies_watched = self.__movie_list(url)
        return self._movies_watched

    @property
    def shows(self):
        """All :class:`Movie`'s in this :class:`User`'s library. Each movie will
        indicate if it's in this :class:`User`'s collection and how many plays
        it has. Protected :class:`User`'s won't return any data unless you are
        friends.
        """
        ext = 'user/library/shows/all.json/{}/{}'.format(trakt.api_key,
                                                         self.username)
        data = self._get_(ext)
        if len(data) > 0:
            self._shows = []
            for show_data in data:
                self._shows.append(TVShow(**show_data))
        return self._shows

    @property
    def show_collection(self):
        """All :class:`Movie`'s in this :class:`User`'s library collection.
        Collection items might include blu-rays, dvds, and digital downloads.
        Protected users won't return any data unless you are friends.
        """
        ext = 'user/library/shows/collection.json/{}/{}'.format(trakt.api_key,
                                                                self.username)
        data = self._get_(ext)
        if len(data) > 0:
            self._show_collection = []
            for show_data in data:
                self._show_collection.append(TVShow(**show_data))
        return self._show_collection

    @property
    def show_watched(self):
        """All :class:`Movie`'s in this :class:`User`'s library collection.
        Collection items might include blu-rays, dvds, and digital downloads.
        Protected users won't return any data unless you are friends.
        """
        ext = 'user/library/shows/watched.json/{}/{}'.format(trakt.api_key,
                                                             self.username)
        data = self._get_(ext)
        if len(data) > 0:
            self._shows_watched = []
            for show_data in data:
                self._shows_watched.append(TVShow(**show_data))
        return self._shows_watched

    @property
    def lists(self):
        """All custom lists for this :class:`User`. Protected :class:`User`'s
        won't return any data unless you are friends. To view your own private
        lists, you will need to authenticate as yourself.
        """
        ext = 'user/lists.json/{}/{}'.format(trakt.api_key, self.username)
        data = self._get_(ext)
        if len(data) > 0:
            self._lists = []
            for list_data in data:
                self._lists.append(UserList(**list_data))
        return self._lists

    @property
    def followers(self):
        """A list of all followers including the since timestamp which is when
        the relationship began. Protected users won't return any data unless
        you are friends. Any friends of the main user that are protected won't
        display data either.
        """
        if self._followers is None:
            ext = 'user/network/followers.json/{}/{}'.format(trakt.api_key,
                                                             self.username)
            data = self._get_(ext)
            self._followers = []
            for user in data:
                self._followers.append(User(**user))
        return self._followers

    @property
    def following(self):
        """A list of all user's this :class:`User` follows including the since
        timestamp which is when the relationship began. Protected users won't
        return any data unless you are friends. Any friends of the main user
        that are protected won't display data either.
        """
        if self._following is None:
            ext = 'user/network/following.json/{}/{}'.format(trakt.api_key,
                                                             self.username)
            data = self._get_(ext)
            self._following = []
            for user in data:
                self._following.append(User(**user))
        return self._following

    @property
    def friends(self):
        """A list of this :class:`User`'s friends (a 2 way relationship where
        each user follows the other) including the since timestamp which is when
        the friendship began. Protected users won't return any data unless you
        are friends. Any friends of the main user that are protected won't
        display data either.
        """
        if self._friends is None:
            ext = 'user/network/friends.json/{}/{}'.format(trakt.api_key,
                                                           self.username)
            data = self._get_(ext)
            self._friends = []
            for user in data:
                self._friends.append(User(**user))
        return self._friends

    @property
    def collected(self):
        """Collected progress for all :class:`TVShow`'s in this
        :class:`User`'s collection.
        """
        if self._collected is None:
            ext = 'user/progress/collected.json/{}/{}/'.format(trakt.api_key,
                                                               self.username)
            data = self._get_(ext)
            self._collected = []
            for show in data:
                self._collected.append(TVShow(**show))
        return self._collected

    @property
    def watched(self):
        """Watched profess for all :class:`TVShow`'s in this :class:`User`'s
        collection.
        """
        if self._watched is None:
            ext = 'user/progress/watched.json/{}/{}/'.format(trakt.api_key,
                                                             self.username)
            data = self._get_(ext)
            self._watched = []
            for show in data:
                self._watched.append(TVShow(**show))
        return self._watched

    @property
    def episode_ratings(self):
        """All :class:`TVEpisodes` this :class:`User` has rated"""
        if self._episode_ratings is None:
            ext = 'user/ratings/episodes.json/{}/{}/'.format(trakt.api_key,
                                                             self.username)
            data = self._get_(ext)
            self._episode_ratings = []
            for episode in data:
                show = episode['show']['title']
                season = episode['episode']['season']
                episode_num = episode['episode']['number']
                flattened_data = {}
                for key, val in episode.items():
                    if isinstance(val, dict):
                        for inner_key, inner_val in val.items():
                            flattened_data[inner_key] = inner_val
                    else:
                        flattened_data[key] = val
                self._episode_ratings.append(TVEpisode(show, season,
                                                       episode_num,
                                                       flattened_data))
        return self._episode_ratings

    @property
    def show_ratings(self):
        """All :class:`TVShow`'s this :class:`User` has rated"""
        if self._show_ratings is None:
            ext = 'user/ratings/shows.json/{}/{}/'.format(trakt.api_key,
                                                          self.username)
            data = self._get_(ext)
            self._show_ratings = []
            for show in data:
                self._show_ratings.append(TVShow(**show))
        return self._show_ratings

    @property
    def movie_ratings(self):
        """All :class:`Movie`'s this :class:`User` has rated"""
        if self._movie_ratings is None:
            ext = 'user/ratings/movies.json/{}/{}/'.format(trakt.api_key,
                                                           self.username)
            data = self._get_(ext)
            self._movie_ratings = []
            for movie in data:
                self._movie_ratings.append(Movie(**movie))
        return self._movie_ratings

    @property
    def episode_watchlist(self):
        """All :class:`TVEpisode`'s this :class:`User`'s watchlist"""
        if self._episode_watchlist is None:
            ext = 'user/watchlist/episodes.json/{}/{}/'.format(trakt.api_key,
                                                               self.username)
            data = self._get_(ext)
            self._episode_watchlist = []
            for episode in data:
                show = episode['show']['title']
                season = episode['episode']['season']
                episode_num = episode['episode']['number']
                flattened_data = {}
                for key, val in episode.items():
                    if isinstance(val, dict):
                        for inner_key, inner_val in val.items():
                            flattened_data[inner_key] = inner_val
                    else:
                        flattened_data[key] = val
                self._episode_watchlist.append(TVEpisode(show, season,
                                                         episode_num,
                                                         flattened_data))
        return self._episode_watchlist

    @property
    def show_watchlist(self):
        """All :class:`TVShow`'s this :class:`User`'s watchlist"""
        if self._show_watchlist is None:
            ext = 'user/watchlist/shows.json/{}/{}/'.format(trakt.api_key,
                                                            self.username)
            data = self._get_(ext)
            self._show_watchlist = []
            for show in data:
                self._show_watchlist.append(TVShow(**show))
        return self._show_watchlist

    @property
    def movie_watchlist(self):
        """All :class:`Movie`'s this :class:`User`'s watchlist"""
        if self._movie_watchlist is None:
            ext = 'user/watchlist/movies.json/{}/{}/'.format(trakt.api_key,
                                                             self.username)
            data = self._get_(ext)
            self._movie_watchlist = []
            for movie in data:
                self._movie_watchlist.append(Movie(**movie))
        return self._movie_watchlist
