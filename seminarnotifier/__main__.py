# -*- config: utf-8 -*-

import logging

def run(config_path, days = 1):
    logging.info('Started')

    with open(config_path, 'r') as config_file:
        import json
        from datetime import datetime, timedelta
        from notifier import Notifier
        from source import Source
        from seminarparser import Parser

        config = json.load(config_file)

        source = Source.get(config['source']['type'], config['source'])
        parser = Parser.get(config['parser']['type'], config['parser'])
        notifier = Notifier.get(config['notifier']['type'], config['notifier'])

        now = datetime.now().date()
        tomorrow = now + timedelta(days = days)

        logging.info('Initialized')

        src = source.get(tomorrow)
        logging.info('Getting source is complete')
        
        headers = parser.find_headers(src)
        logging.info('%d headers found' % len(headers))

        defaults = config['defaults']
        seminars = [parser.parse_seminar(header, defaults) for header in headers]
        logging.info('%d seminars found' % len(headers))


        for seminar in [(seminar.title, datetime.combine(seminar.date, seminar.time).isoformat(' '), seminar.place, '/'.join(seminar.contents)) for seminar in seminars]:
            logging.debug('Seminar found: %s, %s, %s, %s' % seminar)

        tomorrow_seminars = [seminar for seminar in seminars if seminar.date == tomorrow]
        logging.info('%d seminars found on %s' % (len(tomorrow_seminars), tomorrow))

        for seminar in tomorrow_seminars:
            notifier.notify(seminar)
            logging.info('Notify sent: %s, %s, %s' % (seminar.title, seminar.date, seminar.time))

    logging.info('Done')

def main():
    import sys
    from getopt import getopt

    optlist, args = getopt(sys.argv[1:], 'c:l:f:a:', ['config=', 'log-level=', 'log-file=', 'advance='])
    optdict = dict(optlist)

    config_file = optdict.get('--config', optdict.get('-c'))
    if not config_file:
        print 'Usage: %s [--log-level=<log level>] [--log-file=<log-file>] --config=<path to config.json>' % sys.argv[0]
        quit(1)

    log_level = optdict.get('--log-level', optdict.get('-l'))
    log_file = optdict.get('--log-file', optdict.get('-f'))

    log_config = {
            'format': '%(asctime)s %(message)s',
            }
    if log_level:
        numeric_level = getattr(logging, log_level.upper())
        if not isinstance(numeric_level, int):
            raise ValueError('Invalid log level: %s' % log_level)
        log_config['level'] = numeric_level
    if log_file:
        log_config['filename'] = log_file
    logging.basicConfig(**log_config)

    try:
        run(config_file, int(optdict.get('--advance', optdict.get('-a', 1))))
    except:
        logging.exception('Uncought exception')
        quit(2)

main()
