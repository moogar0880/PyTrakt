# -*- coding: utf-8 -*-
from trakt.people import Person


def test_get_person():
    bryan = Person('Bryan Cranston')
    assert bryan.name == 'Bryan Cranston'
    assert bryan.birthday == '1956-03-07'
    assert bryan.death is None
    assert bryan.birthplace == 'San Fernando Valley, California, USA'
    assert bryan.homepage == 'http://www.bryancranston.com/'


def test_get_person_images():
    bryan = Person('Bryan Cranston')
    assert isinstance(bryan.images, dict)


def test_person_magic_methods():
    bryan = Person('Bryan Cranston')
    assert str(bryan) == '<Person>: {name}'.format(name=bryan.name)
    assert str(bryan) == repr(bryan)
