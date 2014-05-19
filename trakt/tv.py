"""Interfaces to all of the TV objects offered by the Trakt.tv API"""
import json
import string
import requests
from datetime import datetime, timedelta

from . import api_key, BaseAPI
from .community import TraktRating, TraktStats
__author__ = 'Jon Nappi'
__all__ = ['trending_shows', 'TVShow', 'TVEpisode', 'TVSeason']


def trending_shows():
    """All :class:`TVShow`'s being watched right now"""
    url = BaseAPI().base_url + '/shows/trending.json/{}'.format(api_key)
    response = requests.get(url)
    data = json.loads(response.content.decode('UTF-8'))
    to_ret = []
    for show in data:
        title = show.get('title')
        to_ret.append(TVShow(title, **show))
    return to_ret


def updated_shows(timestamp=None):
    """All :class:`TVShow`'s updated since *timestamp* (PST). To establish a
    baseline timestamp, you can use the server/time method. It's recommended to
    store the timestamp so you can be efficient in using this method.
    """
    y_day = datetime.now() - timedelta(1)
    ts = timestamp or int(y_day.strftime('%s')) * 1000
    url = BaseAPI().base_url + '/shows/updated.json/{}/{}'.format(api_key, ts)
    response = requests.get(url)
    data = json.loads(response.content.decode('UTF-8'))
    # to_ret = []
    # for show in data['shows']:
    #     title = show.get('title')
    #     to_ret.append(TVShow(title, **show))
    return data['shows']


class TVShow(BaseAPI):
    """A Class representing a TV Show object
    TODO: library
          watching
          episode/library
          episode/seen
          episode/unlibrary
          episode/unseen
          episode/watchingnow
    """
    def __init__(self, title='', **kwargs):
        super(TVShow, self).__init__()
        self.url = self.base_url + 'show/'
        self.top_watchers = None
        self.top_episodes = None
        self.seasons = []
        self.title = title
        if len(kwargs) > 0:
            for key, val in kwargs.items():
                setattr(self, key, val)
        else:
            self.search(show_title=self.title)

    def cancel_watching(self):
        """Cancel watching the current show"""
        url = self.url + 'cancelwatching/' + api_key
        response = requests.get(url)
        if response.status_code == 200:
            pass

    def scrobble(self):
        """Scrobble the current show"""
        url = self.url + 'scrobble/' + api_key
        response = requests.get(url)
        if response.status_code == 200:
            pass

    def watching_now(self):
        """Returns a list of users currently watching this show"""
        url = self.url + 'watchingnow.json/' + api_key + '/' + self.title
        response = requests.get(url)
        if response.status_code == 200:
            pass

    def add_to_library(self):
        """Add this show to your library"""
        pass

    def __fetch_top_watchers(self):
        show_title = self.title
        show_title = string.replace(show_title, ' ', '-')
        url = self.url + 'summary.json/' + api_key + '/' + show_title
        response = requests.get(url)
        if response.status_code == 200:
            data = json.loads(response.content)
            if data is not None:
                self.top_watchers = data['top_watchers']
        return self.top_watchers or None

    def get_top_watchers(self):
        if self.top_watchers is not None:
            return self.top_watchers
        return self.__fetch_top_watchers()

    def __fetch_top_episodes(self):
        show_title = self.title
        show_title = string.replace(show_title, ' ', '-').lower()
        url = self.url + 'summary.json/' + api_key + '/' + show_title
        response = requests.get(url)
        if response.status_code == 200:
            data = json.loads(response.content)
            if data is not None:
                self.top_episodes = data['top_episodes']
        return self.top_episodes

    def get_top_episodes(self):
        if self.top_episodes is not None:
            return self.top_episodes
        return self.__fetch_top_episodes()

    def search(self, show_title=None):
        """Search for general information on a show"""
        show_title = string.replace(show_title, ' ', '-').lower()
        url = self.url + 'summary.json/' + api_key + '/' + show_title
        response = requests.get(url)
        data = None
        if response.status_code == 200:
            data = json.loads(response.content)
        if data is not None:
            for key, val in data.items():
                if key == 'ratings':
                    setattr(self, 'rating', TraktRating(val))
                elif key == 'stats':
                    setattr(self, 'stats', TraktStats(val))
                else:
                    setattr(self, key, val)

    def search_season(self, season_num=None):
        """Search for a show in the Trakt.tv API and store all seasons for this
        show
        """
        try:
            self.seasons[season_num] = TVSeason(self.title, season_num)
        except IndexError:
            while len(self.seasons) < season_num + 1:
                self.seasons.append(None)
            self.seasons[season_num] = TVSeason(self.title, season_num)
        return self.seasons[season_num] or None

    def get_season(self, season_num):
        """Get the requested season"""
        if season_num < 0 or season_num >= len(self.seasons):
            raise Exception
        return self.seasons[season_num-1]


class TVSeason(BaseAPI):
    """Container for TV Seasons"""
    def __init__(self, show, season=1):
        super(TVSeason, self).__init__()
        self.show = show
        self.season = season
        self.episodes = []
        self.url_extension = 'show/season.json/' + api_key
        self.episodes = []
        self.search(self.show, self.season)

    def search(self, show_title, season_num):
        """Search for a tv season"""
        url = self.base_url + self.url_extension + '/'
        # Need to remove spaces and parentheses from show title
        title = string.replace(show_title, ' ', '-').lower()
        title = string.replace(title, '(', '')
        title = string.replace(title, ')', '')
        url += title + '/' + str(season_num)
        response = requests.get(url)
        data = None
        if response.status_code == 200:
            data = json.loads(response.content)
        if data is not None:
            for episode_data in data:
                self.episodes.append(TVEpisode(self.show, self.season,
                                               episode_data=episode_data))

    def __repr__(self):
        title = [self.show, 'Season', self.season]
        title = map(str, title)
        return ' '.join(title)


class TVEpisode(BaseAPI):
    """Container for TV Episodes"""
    def __init__(self, show, season, episode_num=-1, episode_data=None):
        super(TVEpisode, self).__init__()
        self.show = show
        self.season = season
        self.episode = episode_num
        self.overview = self.title = None
        if episode_data is None and episode_num == -1:
            # Do nothing, not enough info given
            pass
        elif episode_num != -1 and episode_data is None:
            self.search(self.show, self.season, self.episode)
        else:  # episode_data != None
            for key, val in episode_data.items():
                if key != 'episode':
                    setattr(self, key, val)
        # if 'overview' in self.__dict__:
            # self.overview = string.replace(self.overview, u'\u2013', '-')
            # self.overview = string.replace(self.overview, u'\u2019', '\'')
            # self.overview = string.replace(self.overview, u'\u2019', '"')

    def search(self, show, season, episode_num):
        pass

    def get_description(self):
        return str(self.overview)

    def comment(self, comment, spoiler=False, review=False):
        """Add a comment (shout or review) to this :class:`TVEpisode` on trakt.
        """
        url = self.base_url + '/comment/episode/{}'.format(api_key)

    def __repr__(self):
        title = map(str, [self.episode, self.title])
        return ' '.join(title)

    __str__ = __repr__

if __name__ == '__main__':
    api_key = '888dbf16c37694fd8633f0f7e423dfc5'
    print api_key
