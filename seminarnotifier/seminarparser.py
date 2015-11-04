# -*- coding: utf-8 -*-

from abc import ABCMeta, abstractmethod

class Parser:
    """
    Abstract class of parser
    """
    __metaclass__ = ABCMeta

    def __init__(self, config):
        """
        Initialized by config dictionary
        """

    @abstractmethod
    def find_headers(self, source):
        """
        Find headers of seminars
        """

    @abstractmethod
    def parse_seminar(self, header):
        """
        Parse seminar from header
        """

    @staticmethod
    def get(source_name, config):
        """
        Get instance of parser implementation
        """

        import util;
        return util.get_class(__name__, source_name, Parser)(config)

class DOMParser(Parser):
    """
    Parser for DOM tree 
    """

    def __init__(self, config):
        """
        Initialized with config dictionary

        config['selector']: XPath selector to find header of seminars
        config['namespaces']: Dictionary of namespaces for XPath
        config['items']: Array of dictionary to parse subitems of seminars
            [n]['selector']: XPath selector to find subitem
            [n]['pattern']: Regexp pattern of subitem (to be contain named groups named 'title', 'date', 'time', 'place' or 'contents')
            [n]['dateformat'], [n]['timeformat']: DateTime format to parse matched 'date' or 'time'
        """
        import re

        self.selector = config.get('selector', '.');
        self.namespaces = config.get('namespaces', {});

        items = config.get('items', []);
        self.items = [{
            'selector': item.get('selector', '.'),
            'pattern': re.compile(item.get('pattern', '.*')),
            'dateformat': item.get('dateformat'),
            'timeformat': item.get('timeformat'),
            } for item in items];

    def find_headers(self, source):
        """
        Find headers of seminars from DOM tree 
        """

        return source.xpath(self.selector, namespaces = self.namespaces);

    def parse_seminar(self, header, defaults = {}):
        """
        Parse seminar from header DOM element
        """
        from datetime import date, datetime
        from seminar import Seminar

        _defaults = Seminar.parse_defaults(defaults)
        seminar = Seminar(**_defaults)

        YEAR_UNDEFINED = datetime.strptime('', '').date().year
        today = date.today()

        for name, value, dateformat, timeformat in [
                (name, match[1], item['dateformat'], item['timeformat'])
                for matches, item in [(item['pattern'].match(e.text), item)
                    for item in self.items
                    for e in header.xpath(item['selector'], namespaces = self.namespaces)]
                if matches
                for match in matches.groupdict().items()
                for name in Seminar.ITEM_NAMES  if match[1] and name == match[0]
                ]:

            if name == 'date':
                value = datetime.strptime(value, dateformat).date()
                if value.year == YEAR_UNDEFINED:
                    value = date(_defaults.get('date', today).year, value.month, value.day)
            elif name == 'time':
                value = datetime.strptime(value, timeformat).time()

            attr = getattr(seminar, name)
            if isinstance(attr, list):
                attr.append(value)
            else:
                setattr(seminar, name, value)

        return seminar
