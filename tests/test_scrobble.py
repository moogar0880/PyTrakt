from trakt.movies import Movie
from trakt.sync import Scrobbler


def test_scrobble():
    guardians = Movie('Guardians of the Galaxy', year=2014, foo='bar')
    scrobbler = Scrobbler(guardians, 0.0, '1.0.0', '2015-02-01')
    scrobbler.start()
    scrobbler.update(50.0)
    scrobbler.pause()
    scrobbler.start()
    scrobbler.stop()
    scrobbler.start()
    scrobbler.finish()


def test_scrobbler_context_manager():
    guardians = Movie('Guardians of the Galaxy', year=2014, foo='bar')
    with Scrobbler(guardians, 0.0, '1.0.0', '2015-02-01') as scrob:
        for i in range(10):
            scrob.update(i*10)
