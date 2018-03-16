import csv

from .cold_call import ColdCall

class ColdCallCollection(object):
    ATTRIBUTES = ['date', 'time', 'name', 'state_code', 'picked_up', 'booked_meeting']

    @classmethod
    def import_from_csv(cls, csv_path):
        calls = []

        with open(csv_path, 'r') as csvfile:
            reader = csv.DictReader(csvfile)

            for row in reader:
                calls.append(ColdCall(
                    date=row['Date'],
                    time=row['Time'],
                    name=row['Who'],
                    state_code=row['Where?'],
                    picked_up=row['Picked up?'] == 'yes',
                    booked_meeting=row['Appointment?'] == 'yes',
                ))

        print('Imported %d cold calls' % len(calls))
        return cls(calls=calls)

    def __init__(self, calls=None):
        if calls:
            self._calls = calls
        else:
            self._calls = []

    def __getitem__(self, key):
        return self._calls[key]

    def append(self, call):
        self._calls.append(call)

    def __str__(self):
        return str([str(call) for call in self._calls])

    def count(self):
        return len(self._calls)

    def picked_up_count(self):
        return len([call for call in self._calls if call.picked_up])

    def meetings_count(self):
        return len([call for call in self._calls if call.booked_meeting])

    def grouped_by_time(self):
        # Aggregate data by hour

        groups = {}

        for call in self._calls:
            key = call.hour

            if key not in groups:
                groups[key] = ColdCallCollection()

            groups[key].append(call)

        return groups
