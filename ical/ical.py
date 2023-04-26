from __future__ import annotations

from datetime import datetime

from icalendar import Calendar, Event
from pytz import UTC

from agu_api.types import Lesson


class Ical:
    @classmethod
    def create_calendar(cls, file_path, group_name) -> Calendar:
        cal = Calendar()
        cal.add('prodid', 'LavroCoder')
        cal.add('X-WR-CALNAME', group_name)
        cal.add('X-WR-TIMEZONE', 'Asia/Novosibirsk')
        cal.add('VERSION', '2.0')

        with open(file_path, 'wb') as f:
            f.write(cal.to_ical())

        return cal

    @classmethod
    def from_file(cls, file_path) -> Calendar:
        with open(file_path, 'rb') as f:
            calendar = Calendar.from_ical(f.read())
        return calendar

    @classmethod
    def save(cls, file_path, calendar):
        with open(file_path, 'wb') as f:
            f.write(calendar.to_ical())

    @staticmethod
    def add_lesson(lesson: Lesson, calendar: Calendar, uid: str) -> Calendar:
        # Название календаря
        calendar_name = calendar.get('X-WR-CALNAME')

        # Название события - название дисциплины
        lesson_discipline_name = "Без названия"
        if lesson.discipline_name is not None:
            lesson_discipline_name = lesson.discipline_name

        if lesson.distant:
            lesson_discipline_name = f"(Д) {lesson_discipline_name}"

        # Название пары
        lesson_name = "Без названия"
        if lesson.name is not None:
            lesson_name = f"{lesson.name}"

        groups = []
        for i, group in enumerate(lesson.groups):
            if "пдг" in group:
                if group[:group.find("(")].strip() == calendar_name:
                    subgroup = group[group.find("("):group.find(")") + 1]
                    lesson_discipline_name = f"{subgroup} {lesson_discipline_name}"
            groups.append(f"{i + 1}. {group.strip()}")

        description = f"{lesson_name}"
        if len(groups):
            groups = "\n".join(groups)
            description += f"\nГруппы:\n{groups}"
        if lesson.teacher_name is not None:
            description += f"\n{lesson.teacher_name}"
        if lesson.distant:
            description += f"\nДистанционно"

        event = Event()
        event.add('summary', lesson_discipline_name)
        event.add('dtstart', datetime(
            lesson.time_begin.year, lesson.time_begin.month, lesson.time_begin.day,
            lesson.time_begin.hour - 7, lesson.time_begin.minute, lesson.time_begin.second,
            tzinfo=UTC
        ))
        event.add('dtend', datetime(
            lesson.time_end.year, lesson.time_end.month, lesson.time_end.day,
            lesson.time_end.hour - 7, lesson.time_end.minute, lesson.time_end.second,
            tzinfo=UTC
        ))
        event.add('dtstamp', datetime.now(tz=UTC))
        event.add('DESCRIPTION', description)
        event.add('LOCATION', lesson.audience)
        event.add('UID', uid)

        calendar.add_component(event)
        return calendar

    @classmethod
    def delete_lesson(cls, calendar: Calendar, uid: str):
        for i, event in enumerate(calendar.subcomponents):
            event_uid = event.get("UID").encode().decode()
            if event_uid == uid:
                calendar.subcomponents.pop(i)
                break
        return calendar

    @classmethod
    def edit_lesson(cls, lesson: Lesson, calendar: Calendar, uid: str):
        calendar = cls.delete_lesson(calendar, uid)
        calendar = cls.add_lesson(lesson, calendar, uid)
        return calendar
