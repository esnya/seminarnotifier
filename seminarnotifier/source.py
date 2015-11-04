# -*- coding: utf-8 -*-

from abc import ABCMeta, abstractmethod

class Source:
    """
    Abstract class of any sources
    """
    __metaclass__ = ABCMeta

    @abstractmethod
    def __init__(self, config):
        """
        Initialized with config dictionary
        """

    @abstractmethod
    def get(self, date):
        """
        Get data source of sepecified date
        """

    @staticmethod
    def get(source_name, config):
        """
        Get instance of data source implementation
        """

        import util;
        return util.get_class(__name__, source_name, Source)(config)

class WebSource(Source):
    """
    Source by web scraping
    """

    def __init__(self, config):
        """
        Initialized with config dictionary

        config['url']: soruce URL

        config['auth']: authentication
            auth['type']: authentication type (now, to be 'basic')
            auth['username']: username
            auth['password']: password
        """

        self.url = config.get('url')

        auth = config.get('auth')
        if auth:
            self.auth = {
                    'type': auth.get('type', 'basic'),
                    'username': auth.get('username'),
                    'password': auth.get('password'),
                    }
        else:
            self.auth = False


    def get_url(self, date):
        """
        Format URL with date
        """

        return date.strftime(self.url)

    def get(self, date):
        """
        Get data
        """
        from lxml import html
        from urllib2 import HTTPBasicAuthHandler, HTTPPasswordMgrWithDefaultRealm, build_opener, urlopen

        url = self.get_url(date)
        if self.auth:
            password_mgr = HTTPPasswordMgrWithDefaultRealm()
            password_mgr.add_password(None, url, self.auth['username'], self.auth['password'])

            handler = HTTPBasicAuthHandler(password_mgr)
            opener = build_opener(handler)

            src = opener.open(url).read()
        else:
            src = urlopen(url).read()

        return html.fromstring(src)
