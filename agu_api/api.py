import requests


class AguApi:
    def __init__(self):
        self.api = 'https://rb.asu.ru/api'

    def method(self, name: object, **kwargs: object) -> object:
        params = kwargs
        response = requests.get(f"{self.api}/{name}", params=params)
        return response.json()

    def timetable(self, sday, time_interval, type, value):
        params = {'sday': sday, 'time_interval': time_interval, 'type': type, 'value': value}
        return self.method('timetable', **params)

    def groups(self):
        return self.method('groups')

    def timetableBG(self, sday=None, time_interval=None, type=None, value=None):
        groups = self.groups()
        groupID = None
        for group in groups:
            if group["SNAME"] == value:
                groupID = group['ID']
                break

        return self.timetable(sday, time_interval, type, groupID)
