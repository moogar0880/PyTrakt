"""A single Interface to the Lists methods offered by the Trakt.tv API"""
from . import api_key, BaseAPI, auth_post
from .tv import TVShow, TVSeason, TVEpisode
from .movies import Movie
__author__ = 'Jon Nappi'
__all__ = ['UserList']


class UserList(BaseAPI):
    """A class type representing a Trakt.tv List"""
    def __init__(self, name, description=None, privacy='private',
                 show_numbers=True, allow_shouts=True, **kwargs):
        """Create a new :class:`UserList` object.

        :param name: The list name. This must be unique across the Trakt.tv
            system.
        :param description: Optional, but recommended, description of what this
            :class:`UserList` contains.
        :param privacy: Privacy level of this :class:`UserList` must be one of
            private, friends, or public.
        :param show_numbers: A boolean flag to determine if this
            :class:`UserList` should show numbers for each item. This is useful
            for ranked lists. Must be True or False
        :param allow_shouts: A boolean flag to determine if this
            :class:`UserList` allows discussion by users who have access. Must
            be True or False
        """
        super(UserList, self).__init__()
        self._name = name
        self._description = description
        self._privacy = privacy
        self._show_numbers = show_numbers
        self._allow_shouts = allow_shouts
        self.slug = None
        self.items = []
        if len(kwargs) > 0:
            for key, val in kwargs:
                setattr(self, key, val)
        else:
            ext = '/lists/add/{}'.format(api_key)
            url = self.base_url + ext
            args = {'name': self._name, 'description': self._description,
                    'privacy': self._privacy, 'show_numbers': self._show_numbers,
                    'allow_shouts': self._allow_shouts}
            real_args = {x: args[x] for x in args if args[x] is not None}
            response = auth_post(url, real_args)
            for key, val in response.items():
                setattr(self, key, val)

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
        ext = '/lists/items/add/{}'.format(api_key)
        url = self.base_url + ext
        args = {'slug': self.slug, 'items': items_list}
        auth_post(url, args)

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
        ext = '/lists/items/delete/{}'.format(api_key)
        url = self.base_url + ext
        args = {'slug': self.slug, 'items': items_list}
        auth_post(url, args)

    def __property_update(self, key, val):
        """Update an attribute of this :class:`UserList`"""
        ext = '/lists/update/{}'.format(api_key)
        url = self.base_url + ext
        args = {'slug': self.slug, key: val}
        auth_post(url, args)
        setattr(self, key, val)

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
        ext = '/lists/delete/{}'.format(api_key)
        url = self.base_url + ext
        args = {'slug': self.slug}
        auth_post(url, args)
