# -*- config: utf-8 -*-

import unittest

def obj(**args):
    return type('<anonymous object>', (object,), args)()

class TestSMTPNotifier(unittest.TestCase):
    def setUp(self):
        import urllib2

        from datetime import date, datetime, time
        from seminarnotifier.notifier import Notifier
        from seminarnotifier.seminar import Seminar

        self.now = datetime.now()

        self.config = {
                'subject': 'Seminar {0} on %B %d',
                'message': 'Seminar {0} on %B %d %H:%M at {2}: \n{1}',
                'host': 'localhost',
                'port': 25,
                'from': '<seminar@mail.example>',
                'to': ['<all@mail.example>'],
                }

        self.notifier = Notifier.get('SMTPNotifier', self.config)

        self.seminar = Seminar('title', date(2015, 4, 15), time(9, 15), 'A111', ['Foo', 'Bar', 'Baz'])

    def test_find_header(self):
        calls = dict()
        class MockSMTP:
            def __init__(*args):
                calls['__init__'] = list(args);
            
            def sendmail(*args):
                calls['sendmail'] = list(args);

            def quit(*args):
                calls['quit'] = list(args);

        import smtplib
        from base64 import b64decode

        smtplib.SMTP = MockSMTP

        self.notifier.notify(self.seminar)

        self.assertEqual(calls['__init__'][1:], ['localhost', 25]);
        self.assertEqual(calls['sendmail'][1:3], ['<seminar@mail.example>', ['<all@mail.example>']]);

        message = calls['sendmail'][3]
        message_body = b64decode(message.split('\n\n')[1].strip())
        self.assertEqual(message_body, 'Seminar title on April 15 09:15 at A111: \nFoo\nBar\nBaz'.encode('UTF-8'))

        self.assertEqual(calls['quit'][1:], []);

