# -*- config: utf-8 -*-


class Seminar:
    """
    Seminar definition
    """

    def __init__(self, title = '', date = None, time = None, place = '', contents = None):
        import datetime

        self.title = title
        self.date = date if date != None else datetime.datetime.now().date()
        self.time = time if time != None else datetime.datetime.now().time()
        self.place = place
        self.contents = contents if contents != None else list()

        if not isinstance(self.date, datetime.date):
            self.date = datetime.date(*tuple(self.date))
        if not isinstance(self.time, datetime.time):
            self.time = datetime.time(*tuple(self.time))

    ITEM_NAMES = ['title', 'date', 'time', 'place', 'contents']

    @staticmethod
    def parse_defaults(defaults = {}):
        """
        Parse dictionary of default values
        """
        import datetime

        _defaults = [(name, defaults[name]) for name in Seminar.ITEM_NAMES if name in defaults]

        _defaults = dict(_defaults)

        if not isinstance(_defaults.get('date'), datetime.date):
            _defaults['date'] = datetime.date(*tuple(_defaults.get('date', [])))
        if not isinstance(_defaults.get('time'), datetime.time):
            _defaults['time'] = datetime.time(*tuple(_defaults.get('time', [])))

        return _defaults
