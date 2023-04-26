from datetime import datetime

import requests

from .types import Lesson, IdSname


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
    def get_id_sname(self, lesson_type) -> list[IdSname]:
        if lesson_type == 1:
            name = "teachers"
        elif lesson_type == 2:
            name = "auditorium"
        else:
            name = "groups"

        result = self.method(name)
        items = []
        for item in result:
            item = IdSname.parse_obj(item)
            items.append(item)
        return items

    def get_lessons(self, lesson_type: str | int, value: str, time_interval: str | int,
                    date: datetime = None) -> list[Lesson]:
        """
        Получает расписание.
        :param lesson_type: Тип расписания (1 - для преподавателей, 2 - для аудитории, 3 - для студентов).
        :param value: Идентификатор преподавателя, аудитории или группы
        :param time_interval: Интервал (1 - день, 2 - неделя, 3 - месяц).
        :param date: Стартовая дата.
        :return: Список пар.
        """
        if date is None:
            date = datetime.now()
        date = date.strftime("%d.%m.%Y")
        time_table = self.timetable(date, time_interval, lesson_type, value)
        lessons = []
        if type(time_table) == list:
            return lessons
        for date, data in time_table.items():
            for lesson_number, lesson in data.items():
                time_begin = datetime.strptime(f"{date} {lesson.get('begin')}", "%d.%m.%y %H:%M")
                time_end = datetime.strptime(f"{date} {lesson.get('end')}", "%d.%m.%y %H:%M")
                for lesson_id, lesson_data in lesson.get('data').items():
                    discipline_name = lesson_data.get('discipline_name')
                    if discipline_name is None:
                        discipline_name = lesson_data.get('disciplinename')
                    lesson = {
                        "id": lesson_id,
                        "time_begin": time_begin,
                        "time_end": time_end,
                        "audience": lesson_data.get('AUDITORIUM'),
                        "groups": lesson_data.get('groupname'),
                        "name": lesson_data.get('lesson_name'),
                        "discipline_name": discipline_name,
                        "teacher_name": lesson_data.get('teacher')[0].get('fio'),
                        "distant": lesson_data.get('Distant')
                    }
                    try:
                        lesson = Lesson.parse_obj(lesson)
                    except Exception as e:
                        print(e)
                    lessons.append(lesson)
        return lessons

    def get_timetable_for_group_for_month(self, group_id: str, date: datetime = None) -> list[Lesson]:
        lessons = self.get_lessons(3, group_id, 3, date)
        return lessons

    def get_lessons_for_current_2_month(self, lesson_type: str | int, value: str) -> list[Lesson]:
        """
        Получает расписание за текущий и следующий месяц.
        :param lesson_type: Тип расписания (1 - для преподавателей, 2 - для аудитории, 3 - для студентов).
        :param value: Идентификатор преподавателя, аудитории или группы.
        :return: Список пар.
        """
        now = datetime.now()  # получаем текущую дату и время
        next_month = now.month + 1 if now.month != 12 else 1  # вычисляем номер следующего месяца
        year = now.year + 1 if next_month == 1 else now.year  # вычисляем год следующего месяца
        now_month_day = datetime(now.year, now.month, 1)  # создаем новую дату с первым числом текущего месяца
        next_month_day = datetime(year, next_month, 1)  # дата с первым число следующего месяца

        lessons = []
        now_month_lessons = self.get_lessons(lesson_type, value, 3, now_month_day)
        next_month_lessons = self.get_lessons(lesson_type, value, 3, next_month_day)
        lessons.extend(now_month_lessons)
        lessons.extend(next_month_lessons)
        return lessons
