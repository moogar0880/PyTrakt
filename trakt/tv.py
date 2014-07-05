"""Interfaces to all of the TV objects offered by the Trakt.tv API"""
from datetime import datetime, timedelta
from operator import itemgetter

from proxy_tools import module_property

from ._core import BaseAPI, auth_post, Genre, Comment
from .community import TraktRating, TraktStats
import trakt
__author__ = 'Jon Nappi'
__all__ = ['trending_shows', 'TVShow', 'TVEpisode', 'TVSeason', 'rate_shows',
           'get_recommended_shows', 'dismiss_recommendation', 'rate_episodes']


def dismiss_recommendation(tvdb_id=None, title=None, year=None):
    """Dismiss the show matching the specified criteria from showing up in
    recommendations.
    """
    ext = 'recommendations/shows/dismiss/{}'.format(trakt.api_key)
    url = BaseAPI().base_url + ext
    args = {'tvdb_id': tvdb_id, 'title': title, 'year': year}
    real_args = {x: args[x] for x in args if args[x] is not None}
    auth_post(url, real_args)


def get_recommended_shows(genre=None, start_year=None, end_year=None,
                          hide_collected=True, hide_watchlisted=True):
    """Get a list of :class:`TVShow`'s recommended based on your watching
    history and your friends. Results are returned with the top recommendation
    first.

    :param genre: Genre slug to filter by. See tv.genres for a list of valid
        genres.
    :param start_year: 4 digit year to filter shows premiering in this year or
        later.
    :param end_year: 4 digit year to filter shows premiering released in this
        year or earlier.
    :param hide_collected: Set to False to show shows the user has collected.
    :param hide_watchlisted: Set to False to show shows on the user's watchlist
    """
    ext = 'recommendations/shows/{}'.format(trakt.api_key)
    args = {'genre': genre, 'start_year': start_year, 'end_year': end_year,
            'hide_collected': hide_collected,
            'hide_watchlisted': hide_watchlisted}
    real_args = {x: args[x] for x in args if args[x] is not None}
    response = BaseAPI()._post_(ext, real_args)
    shows = []
    for show in response:
        shows.append(TVShow(**show))
    return shows


def rate_shows(shows, rating):
    """Apply *rating* to all :class:`TVShow`'s in *shows*"""
    valid_ratings = ['love', 'hate', 'unrate'] + list(range(11))
    if rating in valid_ratings:
        ext = 'rate/shows/{}'.format(trakt.api_key)
        show_list = []
        for show in shows:
            d = {'tvdb_id': show.tvdb_id, 'title': show.title,
                 'year': show.year, 'rating': rating}
            show_list.append(d)
        args = {'shows': show_list}
        BaseAPI()._post_(ext, args)


def rate_episodes(episodes, rating):
    """Apply *rating* to all :class:`TVEpisode`'s in *episodes*"""
    valid_ratings = ['love', 'hate', 'unrate'] + list(range(11))
    if rating in valid_ratings:
        ext = 'rate/episodes/{}'.format(trakt.api_key)
        episode_list = []
        for episode in episodes:
            d = {'tvdb_id': episode.tvdb_id, 'title': episode.title,
                 'year': episode.year, 'season': episode.season,
                 'episode': episode.episode, 'rating': rating}
            episode_list.append(d)
        args = {'episodes': episode_list}
        BaseAPI()._post_(ext, args)


@module_property
def genres():
    """A list of all possible :class:`Movie` Genres"""
    ext = 'genres/shows.json/{}'.format(trakt.api_key)
    data = BaseAPI()._get_(ext)
    genres = []
    for genre in data:
        genres.append(Genre(genre['name'], genre['slug']))
    return genres


@module_property
def trending_shows():
    """All :class:`TVShow`'s being watched right now"""
    ext = 'shows/trending.json/{}'.format(trakt.api_key)
    data = BaseAPI()._get_(ext)
    to_ret = []
    for show in data:
        title = show.get('title')
        to_ret.append(TVShow(title, **show))
    return to_ret


@module_property
def updated_shows(timestamp=None):
    """All :class:`TVShow`'s updated since *timestamp* (PST). To establish a
    baseline timestamp, you can use the server/time method. It's recommended to
    store the timestamp so you can be efficient in using this method.
    """
    y_day = datetime.now() - timedelta(1)
    ts = timestamp or int(y_day.strftime('%s')) * 1000
    ext = 'shows/updated.json/{}/{}'.format(trakt.api_key, ts)
    data = BaseAPI()._get_(ext)
    to_ret = []
    for show in data['shows']:
        title = show.get('title')
        to_ret.append(TVShow(title, **show))
    return to_ret


class TVShow(BaseAPI):
    """A Class representing a TV Show object"""
    def __init__(self, title='', **kwargs):
        super(TVShow, self).__init__()
        self.top_watchers = self.top_episodes = self.year = self.tvdb_id = None
        self.imdb_id = self.genres = self.certification = None
        self.network = None
        self.seasons = []
        self.people = []
        self.title = title
        if len(kwargs) > 0:
            for key, val in kwargs.items():
                setattr(self, key, val)
        else:
            self.search()

    def cancel_watching(self):
        """Cancel watching the current show"""
        ext = 'cancelwatching/{}'.format(trakt.api_key)
        self._get_(ext)

    def scrobble(self):
        """Scrobble the current show"""
        ext = 'scrobble/{}'.format(trakt.api_key)
        self._get_(ext)

    def watching_now(self):
        """Returns a list of users currently watching this show"""
        ext = 'watchingnow.json/{}/{}'.format(trakt.api_key, self.title)
        self._get_(ext)

    def rate(self, rating):
        """Rate this :class:`TVShow` on trakt. Depending on the current users
        settings, this may also send out social updates to facebook, twitter,
        tumblr, and path.
        """
        valid_ratings = ['love', 'hate', 'unrate'] + list(range(11))
        if rating in valid_ratings:
            ext = 'rate/show/{}'.format(trakt.api_key)
            args = {'rating': rating, 'tvdb_id': self.tvdb_id,
                    'title': self.title, 'year': self.year}
            self._post_(ext, args)

    def __fetch_top_watchers(self):
        """Handle fetching the top watchers of this show"""
        show_title = self.title.replace(' ', '-')
        ext = 'summary.json/{}/{}'.format(trakt.api_key, show_title)
        data = self._get_(ext)
        self.top_watchers = data['top_watchers']
        return self.top_watchers or None

    def get_top_watchers(self):
        """Return the list of most active watchers of this :class:`TVShow`"""
        if self.top_watchers is not None:
            return self.top_watchers
        return self.__fetch_top_watchers()

    def __fetch_top_episodes(self):
        """Handle fetching top episodes list"""
        show_title = self.title.replace(' ', '-').lower()
        ext = 'summary.json/{}/{}'.format(trakt.api_key, show_title)
        data = self._get_(ext)
        self.top_episodes = data['top_episodes']
        return self.top_episodes

    def get_top_episodes(self):
        """Return the list of top rated episodes for this :class:`TVShow`"""
        if self.top_episodes is not None:
            return self.top_episodes
        return self.__fetch_top_episodes()

    @property
    def _search_title(self):
        """The title of this :class:`TVShow` formatted in a searchable way"""
        return self.title.replace(' ', '-').lower()

    def search(self):
        """Search for general information on a show"""
        from .users import User
        from .people import Person
        ext = 'search/shows.json/{}/{}'.format(trakt.api_key,
                                               self._search_title)
        args = {'query': self._search_title, 'seasons': True}
        data = self._get_(ext, args)
        for response in data:
            if response['title'] == self.title:
                data = response
                break
        for key, val in data.items():
            if key == 'ratings':
                setattr(self, 'rating', TraktRating(val))
            elif key == 'stats':
                setattr(self, 'stats', TraktStats(val))
            elif key == 'top_episodes':
                self.top_episodes = []
                for episode in val:
                    show = self.title
                    season = episode.pop('season')
                    episode_num = episode.pop('number')
                    self.top_episodes.append(TVEpisode(show, season,
                                                       episode_num, episode))
            elif key == 'top_watchers':
                self.top_watchers = []
                for user in val:
                    self.top_watchers.append(User(**user))
            elif key == 'people':
                self.people = []
                for person in val['actors']:
                    self.people.append(Person(**person))
            elif key == 'genres':
                self.genres = []
                for genre in val:
                    slug = genre.lower().replace(' ', '-')
                    self.genres.append(Genre(genre, slug))
            elif key == 'seasons':
                self.seasons = []
                sorted_val = sorted(val, key=itemgetter('season'))
                results = [s['season'] for s in sorted_val]
                # Special check for shows with no "Specials" season
                if 0 not in results:
                    self.seasons.append(TVSeason(self.title, season=0))
                for season in sorted_val:
                    season_num = season.get('season', 0)
                    self.seasons.append(TVSeason(self.title, season=season_num))
            else:
                setattr(self, key, val)
        # For now it looks like the API doesn't return all the data we need on
        # search, so we'll need to do an explicit search for missing data
        if len(self.people) == 0:
            ext = 'show/summary.json/{}/{}'.format(trakt.api_key,
                                                   self._search_title)
            data = self._get_(ext)
            people = data['people'].pop('actors', [])
            self.people = []
            for person in people:
                self.people.append(Person(**person))

    def seen(self):
        """Mark this :class:`TVShow` as seen"""
        ext = 'show/seen/{}'.format(trakt.api_key)
        args = {'imdb_id': self.imdb_id, 'tvdb_id': self.tvdb_id,
                'title': self.title, 'year': self.year}
        self._post_(ext, args)

    def add_to_library(self):
        """Add this :class:`TVShow` to the current :class:`User`'s library"""
        ext = 'show/library/{}'.format(trakt.api_key)
        args = {'imdb_id': self.imdb_id, 'tvdb_id': self.tvdb_id,
                'title': self.title, 'year': self.year}
        self._post_(ext, args)

    def comment(self, comment, spoiler=False, review=False):
        """Add a comment (shout or review) to this :class:`Move` on trakt."""
        ext = '/comment/episode/{}'.format(trakt.api_key)
        args = {'title': self.title, 'year': self.year, 'comment': comment,
                'spoiler': spoiler, 'review': review}
        if self.tvdb_id == '' or self.tvdb_id is None:
            args['imdb_id'] = self.imdb_id
        else:
            args['tvdb_id'] = self.tvdb_id
        self._post_(ext, args)

    @property
    def comments(self):
        """All comments (shouts and reviews) for this :class:`Movie`. Most
        recent comments returned first.
        """
        from .users import User
        ext = 'show/comments.json/{}/{}/{}'.format(trakt.api_key,
                                                   self._search_title, 'all')
        data = self._get_(ext)
        comments = []
        for comment in data:
            user = User(**comment.pop('user'))
            ratings = comment.pop('user_ratings')
            comments.append(Comment(user=user, user_ratings=ratings, **comment))
        return comments

    def dismiss(self):
        """Dismiss this movie from showing up in Movie Recommendations"""
        dismiss_recommendation(tvdb_id=self.tvdb_id, title=self.title,
                               year=self.year)

    def __str__(self):
        """Return a string representation of a :class:`TVShow`"""
        return '<TVShow> {}'.format(self.title.encode('ascii', 'ignore'))
    __repr__ = __str__

    @property
    def _list_json(self):
        """JSON representation of this :class:`TVShow`"""
        return {'type': 'show', 'tvdb_id': self.tvdb_id, 'title': self.title}


class TVSeason(BaseAPI):
    """Container for TV Seasons"""
    def __init__(self, show, season=1):
        super(TVSeason, self).__init__()
        self.show = show
        self.season = season
        self.episodes = []
        self.tvdb_id = self.imdb_id = None
        self.search(self.show, self.season)

    def search(self, show_title, season_num):
        """Search for a tv season"""
        ext = 'show/season.json/{}/'.format(trakt.api_key)
        # Need to remove spaces and parentheses from show title
        title = show_title.replace(' ', '-').replace('(', '').replace(')', '')
        title = title.lower()
        ext += title + '/' + str(season_num)
        data = self._get_(ext)
        for episode_data in data:
            self.episodes.append(TVEpisode(self.show, self.season,
                                           episode_data=episode_data))

    def seen(self):
        """Mark this :class:`TVSeason` as seen"""
        ext = 'show/season/seen/{}'.format(trakt.api_key)
        args = {'imdb_id': self.imdb_id, 'tvdb_id': self.tvdb_id,
                'title': self.show, 'year': self.show.year,
                'season': self.season}
        self._post_(ext, args)

    def add_to_library(self):
        """Add this :class:`TVSeason` to the current :class:`User`'s library"""
        ext = 'show/season/library/{}'.format(trakt.api_key)
        args = {'imdb_id': self.imdb_id, 'tvdb_id': self.tvdb_id,
                'title': self.show, 'year': self.show.year,
                'season': self.season}
        self._post_(ext, args)

    def __str__(self):
        title = ['<TVSeason>:', self.show, 'Season', self.season]
        title = map(str, title)
        return ' '.join(title)
    __repr__ = __str__

    @property
    def _list_json(self):
        """JSON representation of this :class:`TVSeason`"""
        return {'type': 'show', 'tvdb_id': self.tvdb_id, 'title': self.show,
                'season': self.season}


class TVEpisode(BaseAPI):
    """Container for TV Episodes"""
    def __init__(self, show, season, episode_num=-1, episode_data=None):
        super(TVEpisode, self).__init__()
        self.show = show
        self.season = season
        self.episode = episode_num
        self.overview = self.title = self.year = self.tvdb_id =  None
        self._stats = self.imdb_id = None
        if episode_data is None and episode_num == -1:
            # Do nothing, not enough info given
            pass
        elif episode_num != -1 and episode_data is None:
            self.search(self.show, self.season, self.episode)
        else:  # episode_data != None
            for key, val in episode_data.items():
                if key != 'episode':
                    setattr(self, key, val)

    def search(self, show, season, episode_num):
        pass

    def get_description(self):
        return str(self.overview)

    def rate(self, rating):
        """Rate this :class:`TVEpisode` on trakt. Depending on the current users
        settings, this may also send out social updates to facebook, twitter,
        tumblr, and path.
        """
        valid_ratings = ['love', 'hate', 'unrate'] + list(range(11))
        if rating in valid_ratings:
            ext = 'rate/episode/{}'.format(trakt.api_key)
            args = {'rating': rating, 'tvdb_id': self.tvdb_id,
                    'title': self.title, 'year': self.year,
                    'season': self.season, 'episode': self.episode}
            self._post_(ext, args)

    def add_to_library(self):
        """Add this :class:`TVEpisode` to your Trakt.tv library"""
        ext = '/show/episode/library/{}'.format(trakt.api_key)
        self._post_(ext, self._standard_args)

    def seen(self):
        """Mark this episode as seen"""
        ext = '/show/episode/seen/{}'.format(trakt.api_key)
        self._post_(ext, self._standard_args)

    @property
    def stats(self):
        """All of the Trakt.tv stats for for this :class:`TVEpisode` including
        all ratings breakdowns, scrobbles, checkins, collections, lists, and
        comments.
        """
        if self._stats is None:
            ext = 'show/episode/stats.json/{}/{}/{}/{}'.format(trakt.api_key,
                                                               self.title,
                                                               self.season,
                                                               self.episode)
            self._stats = self._get_(ext)
        return self._stats

    @property
    def summary(self):
        """All information for this :class:`TVEpisode`, including ratings."""
        ext = '/show/episode/summary.json/{}/{}/{}/{}'.format(trakt.api_key,
                                                              self.title,
                                                              self.season,
                                                              self.episode)
        return self._get_(ext)

    def remove_from_library(self):
        """Remove this :class:`TVEpisode` from your library"""
        ext = '/show/episode/unlibrary/{}'.format(trakt.api_key)
        return self._post_(ext, self._standard_args)

    def mark_unseen(self):
        """Remove this :class:`TVEpisode` from your library"""
        ext = '/show/episode/unseen/{}'.format(trakt.api_key)
        return self._post_(ext, self._standard_args)

    def remove_from_watchlist(self):
        """Remove this :class:`TVEpisode` from your watchlist"""
        ext = '/show/episode/unwatchlist/{}'.format(trakt.api_key)
        return self._post_(ext, self._standard_args)

    def add_to_watchlist(self):
        """Add this :class:`TVEpisode` to your watchlist"""
        ext = '/show/episode/watchlist/{}'.format(trakt.api_key)
        return self._post_(ext, self._standard_args)

    def comment(self, comment, spoiler=False, review=False):
        """Add a comment (shout or review) to this :class:`TVEpisode` on trakt.
        """
        ext = 'comment/episode/{}'.format(trakt.api_key)
        args = {'title': self.show, 'year': self.year, 'season': self.season,
                'episode': self.title, 'comment': comment, 'spoiler': spoiler,
                'review': review}
        if self.tvdb_id == '' or self.tvdb_id is None:
            args['imdb_id'] = self.imdb_id
        else:
            args['tvdb_id'] = self.tvdb_id
        self._post_(ext, args)

    @property
    def comments(self):
        """All comments (shouts and reviews) for this :class:`Movie`. Most
        recent comments returned first.
        """
        from .users import User
        ext = 'show/episode/comments.json/{}/{}/{}/{}/{}'.format(trakt.api_key,
                                                                 self.title,
                                                                 self.season,
                                                                 self.episode,
                                                                 'all')
        data = self._get_(ext)
        comments = []
        for comment in data:
            user = User(**comment.get('user'))
            ratings = comment.get('user_ratings')
            comments.append(Comment(user=user, user_ratings=ratings, **comment))
        return comments

    @property
    def watching_now(self):
        """A `list` of :class:`User`'s currently watching this
        :class:`TVEpisode`
        """
        from .users import User
        ext = 'show/episode/comments.json/{}/{}/{}/{}'.format(trakt.api_key,
                                                              self.title,
                                                              self.season,
                                                              self.episode)
        data = self._get_(ext)
        users = []
        for user in data:
            users.append(User(**user))
        return users

    def __repr__(self):
        return '<TVEpisode>: {} S{}E{} {}'.format(self.show, self.season,
                                                  self.episode, self.title)
    __str__ = __repr__

    @property
    def _list_json(self):
        """JSON representation of this :class:`TVEpisode`"""
        return {'type': 'show', 'tvdb_id': self.tvdb_id, 'title': self.show,
                'season': self.season, 'episode': self.episode}

    @property
    def _standard_args(self):
        """JSON representation of this :class:`TVEpisode` as used by several
        method calls
        """
        return {'imdb_id': self.imdb_id, 'tvdb_id': self.tvdb_id,
                'title': self.title, 'year': self.year,
                'episodes': [{'season': self.season, 'episode': self.episode}]}
