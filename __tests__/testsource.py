# -*- config: utf-8 -*-

import unittest

def obj(**args):
    return type('<anonymous object>', (object,), args)()

class TestWebSource(unittest.TestCase):
    def setUp(self):
        import urllib2

        from datetime import datetime
        from seminarnotifier.source import Source

        urllib2.urlopen = lambda url: obj(read = lambda _self: self.urlopen_result)
        self.urlopen_result = 'result'

        self.now = datetime.now()

        self.config = {
                'url': 'http://www.example/seminar/%%/%Y/%m',
                }
        self.source = Source.get('WebSource', self.config)

    def test_get_url(self):
        from datetime import datetime
        date = datetime(1999, 6, 12)

        url = self.source.get_url(date)
        self.assertEqual(url, 'http://www.example/seminar/%/1999/06')

    def test_get(self):
        self.urlopen_result = '<html><head></head><body><div id="foo">bar</div></body></html>'

        doc = self.source.get(self.now)

        self.assertEqual(doc.tag, 'html')
        self.assertEqual(doc[1].tag, 'body')
        self.assertEqual(doc[1][0].tag, 'div')
        self.assertEqual(doc[1][0].get('id'), 'foo')
        self.assertEqual(doc[1][0].text, 'bar')
