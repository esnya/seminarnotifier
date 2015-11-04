# -*- coding: utf-8 -*-


from abc import ABCMeta, abstractmethod

class Notifier:
    """
    Abstract class of notifier
    """
    __metaclass__ = ABCMeta

    def __init__(self, config):
        """
        Initialized by config dictionary
        """

    @abstractmethod
    def notify(self, seminar):
        """
        Notify seminar
        """

    @staticmethod
    def get(source_name, config):
        """
        Get instance of notifier implementation
        """

        import util;
        return util.get_class(__name__, source_name, Notifier)(config)

class SMTPNotifier(Notifier):
    """
    Send mail notifier
    """
    def __init__(self, config):
        """
        Initialized by config dictionary

        config['subject']: Subject for e-mail
        config['message']: Message body for e-mail

        DateTime format, '{0}' (title), '{1}' (contents) and '{2}' (place) are available in 'subject' and 'message'.
        followings are SMTP config...

        config['host']
        config['port']
        config['from']
        config['to'][]
        """

        self.subject = config.get('subject')
        self.message = config.get('message')

        self.host = config.get('host', 'localhost')
        self.port = config.get('port', 25)
        self.from_ = config.get('from')
        self.to = config.get('to')

    def notify(self, seminar):
        """
        Notify seminar
        """
        import re 
        from datetime import datetime
        from smtplib import SMTP
        from email.mime.text import MIMEText
        from email.header import Header

        dt = datetime.combine(seminar.date, seminar.time)

        format_values = (seminar.title, '\n'.join(seminar.contents), seminar.place)
        datetime_formatter = lambda matches: dt.strftime(matches.group(0))
        datetime_pattern = re.compile('%-?[a-zA-Z]')

        message_body = datetime_pattern.sub(datetime_formatter, self.message.format(*format_values))

        message = MIMEText(message_body, _charset = 'UTF-8')
        message['Subject'] = Header(datetime_pattern.sub(datetime_formatter, self.subject.format(*format_values)), 'UTF-8').encode()
        message['From'] = self.from_
        message['To'] = ', '.join(self.to)

        smtp = SMTP(self.host, self.port)
        smtp.sendmail(self.from_, self.to, message.as_string())
        smtp.quit()

