from datetime import datetime

import requests

from .types import Group, Lesson


class AguApi:
    def __init__(self):
        self.api = 'https://rb.asu.ru/api'

    def method(self, name: object, **kwargs: object):
        params = kwargs
        response = requests.get(f"{self.api}/{name}", params=params)
        return response.json()

    def timetable(self, sday, time_interval, type, value):
        params = {'sday': sday, 'time_interval': time_interval, 'type': type, 'value': value}
        return self.method('timetable', **params)

    def groups(self) -> list[dict]:
        return self.method('groups')

    def timetableBG(self, sday=None, time_interval=None, type=None, value=None):
        groups = self.groups()
        groupID = None
        for group in groups:
            if group["SNAME"] == value:
                groupID = group['ID']
                break

        return self.timetable(sday, time_interval, type, groupID)


class Agu(AguApi):
    def get_groups(self) -> list[Group]:
        groups = []
        for item in self.groups():
            group = Group.parse_obj(item)
            groups.append(group)
        return groups

    def get_timetable_for_group_for_month(self, group_id: str, date: datetime = None) -> list[Lesson]:
        if date is None:
            date = datetime.now()
        date = date.strftime("%d.%m.%y")
        time_table = self.timetable(date, 3, 3, group_id)
        lessons = []
        for date, data in time_table.items():
            for lesson_number, lesson in data.items():
                time_begin = datetime.strptime(f"{date} {lesson.get('begin')}", "%d.%m.%y %H:%M")
                time_end = datetime.strptime(f"{date} {lesson.get('end')}", "%d.%m.%y %H:%M")
                for lesson_id, lesson_data in lesson.get('data').items():
                    lesson = {
                        "id": lesson_id,
                        "time_begin": time_begin,
                        "time_end": time_end,
                        "audience": lesson_data.get('AUDITORIUM'),
                        "groups": lesson_data.get('groupname'),
                        "name": lesson_data.get('lesson_name'),
                        "discipline_name": lesson_data.get('disciplinename'),
                        "teacher_name": lesson_data.get('teacher')[0].get('fio'),
                        "distant": lesson_data.get('Distant')
                    }
                    lesson = Lesson.parse_obj(lesson)
                    lessons.append(lesson)
        return lessons
