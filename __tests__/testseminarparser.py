# -*- config: utf-8 -*-

import unittest

def obj(**args):
    return type('<anonymous object>', (object,), args)()

class TestDOMParser(unittest.TestCase):
    def setUp(self):
        import urllib2

        from datetime import datetime
        from seminarnotifier.seminarparser import Parser

        self.now = datetime.now()

        self.config = {
                'selector': '//h1',
                'namespaces': { 're': 'http://exslt.org/regular-expressions' },
                'items': [
                    {
                        'selector': '.',
                        'pattern': '(?P<title>.*?) on (?P<date>[A-Z][a-z]+ [0-9]+)( @(?P<place>.*))?',
                        'dateformat': '%B %d',
                    },
                    {
                        'selector': 'following-sibling::ul[1]/li[re:match(text(), "Time: ")]',
                        'pattern': 'Time: (?P<time>[0-9]+:[0-9]+)-?',
                        'timeformat': '%H:%M',
                    },
                    {
                        'selector': 'following-sibling::ul[1]/li[re:match(text(), "Contents")]/ul/li',
                        'pattern': '(?P<contents>.*)',
                    },
                    ],
                }
        self.parser = Parser.get('DOMParser', self.config)

    def test_find_header(self):
        from lxml import html

        doc = html.fromstring('<!DOCTYPE html>'
                + ' <html>' 
                + ' <body>' 
                + '     <h1>Seminar 1</h1>' 
                + '     <h2>Subtitle</h2>' 
                + '     <ul><li>Time: 9:00-12:00</li><li>Contents: <ul><li>Foo1</li><li>Foo2</li></ul></li></ul>' 
                + '     <h1>Seminar 2</h1>' 
                + '     <h2>Subtitle 2</h2>' 
                + '     <ul><li>Time: 9:00-13:00</li><li>Contents:</ul>' 
                + '     <h1>Seminar 3</h1>' 
                + '     <h2>Subtitle</h2>' 
                + '     <ul><li>Time: 14:00-16:00</li><li>Contents: <ul><li>Baz1</li></ul>' 
                + ' </body>' 
                + ' </html>')

        headers = self.parser.find_headers(doc)

        self.assertEqual(set(map(lambda e: e.tag, headers)), set(['h1']))
        self.assertEqual(map(lambda e: e.text, headers), ['Seminar 1', 'Seminar 2', 'Seminar 3'])

    def test_parse_seminar(self):
        from lxml import html
        from datetime import date, datetime, time

        doc = html.fromstring('<!DOCTYPE html>'
                + ' <html>' 
                + ' <body>' 
                + '     <h1>Seminar 1 on June 1</h1>' 
                + '     <h2>Subtitle</h2>' 
                + '     <ul><li>Time: 9:00-12:00</li><li>Contents<ul><li>Foo1</li><li>Foo2</li></ul></li></ul>' 
                + '     <h1>Seminar 2 on June 8</h1>' 
                + '     <h2>Subtitle 2</h2>' 
                + '     <ul><li>Time: 14:15-16:00</li><li>Contents</ul>' 
                + '     <h1>Seminar 3 on July 5 @A301</h1>' 
                + '     <h2>Subtitle</h2>' 
                + '     <ul><li>Contents<ul><li>Baz1</li></ul>' 
                + ' </body>' 
                + ' </html>')

        defaults = {
                'place': 'A101',
                'time': time(8, 0),
                'date': date(2000, 1, 1)
                }

        seminars = [self.parser.parse_seminar(header, defaults) for header in self.parser.find_headers(doc)]

        self.assertEqual(seminars[0].title, 'Seminar 1')
        self.assertEqual(seminars[0].date, date(2000, 6, 1))
        self.assertEqual(seminars[0].time, time(9, 0))
        self.assertEqual(seminars[0].place, 'A101')
        self.assertEqual(seminars[0].contents, ['Foo1', 'Foo2'])

        self.assertEqual(seminars[1].title, 'Seminar 2')
        self.assertEqual(seminars[1].date, date(2000, 6, 8))
        self.assertEqual(seminars[1].time, time(14, 15))
        self.assertEqual(seminars[1].place, 'A101')
        self.assertEqual(seminars[1].contents, [])

        self.assertEqual(seminars[2].title, 'Seminar 3')
        self.assertEqual(seminars[2].date, date(2000, 7, 5))
        self.assertEqual(seminars[2].time, time(8, 0))
        self.assertEqual(seminars[2].place, 'A301')
        self.assertEqual(seminars[2].contents, ['Baz1'])
