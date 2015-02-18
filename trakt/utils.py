# -*- coding: utf-8 -*-
import re
import sys
import unicodedata
from datetime import datetime

__author__ = 'Jon Nappi'


def slugify(value):
    """Converts to lowercase, removes non-word characters (alphanumerics and
    underscores) and converts spaces to hyphens. Also strips leading and
    trailing whitespace.

    Adapted from django.utils.text.slugify
    """
    if sys.version_info[0] == 2:
        value = unicode(value)
    value = unicodedata.normalize('NFKD',
                                  value).encode('ascii',
                                                'ignore').decode('ascii')
    value = re.sub('[^\w\s-]', '', value).strip().lower()
    return re.sub('[-\s]+', '-', value)


def airs_date(airs_at):
    """convert a timestamp of the form '2015-02-01T05:30:00.000-08:00' to a
    python datetime object (with time zone information removed)
    """
    convertable = '-'.join(airs_at.split('-')[:-1])
    return datetime.strptime(convertable, '%Y-%m-%dT%H:%M:%S.000')


def now():
    """Get the current day in the format expected by each :class:`Calendar`"""
    meow = datetime.now()
    year = meow.year
    month = meow.month if meow.month > 10 else '0{}'.format(meow.month)
    day = meow.day if meow.day > 10 else '0{}'.format(meow.day)
    return '{}-{}-{}'.format(year, month, day)


def extract_ids(id_dict):
    """Extract the inner `ids` dict out of trakt JSON responses and insert them
    into the containing `dict`. Then return the input `dict`
    """
    id_dict.update(id_dict.pop('ids', {}))
    return id_dict


class Paginator(list):
    def __init__(self, iterable, page_size=10):
        super(Paginator, self).__init__(iterable)
        self.page, self.page_size = 1, page_size
