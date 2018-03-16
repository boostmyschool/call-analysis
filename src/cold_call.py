from dateutil import parser

class ColdCall(object):
    ATTRIBUTES = ['name', 'state_code', 'picked_up', 'booked_meeting']

    def __init__(self, date, time, **kwargs):
        self._attrs = {}
        self._attrs.update(kwargs)

        self.datetime = parser.parse('%s %s' % (date, time))

    def __getattr__(self, name):
        if name in self.ATTRIBUTES:
            return self._attrs[name]

        raise NameError('name \'%s\' is not defined' % name)

    def __str__(self):
        print('here')
        return str(self._attrs)

    @property
    def hour(self):
        return self.datetime.hour
