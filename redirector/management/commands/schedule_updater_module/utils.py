import time
import traceback

from django.conf import settings
from loguru import logger

from agu_api import AguApi
from agu_api.types import Lesson
from calendar_api import GoogleCalendar, AguGoogleCalendar
from redirector.models import GroupCalendar, Schedule


def get_or_create_calendars(agu_group_id: str, agu_group_name: str) -> GroupCalendar:
    """
    Создает календарь и добавляет его в базу данных, если он не существует.
    :return: Объект GroupCalendar.
    """
    group_calendar = GroupCalendar.get_by_agu_id(agu_group_id)
    if group_calendar is None:
        logger.debug("Create google calendar")
        google_calendar = GoogleCalendar(settings.GOOGLE_SECRET_FILE_PATH)
        try:
            gc_group = google_calendar.create_calendar(agu_group_name)
        except Exception as e:
            logger.warning("%s" % e)
            logger.warning(traceback.format_exc())
            logger.debug("Waiting 60 seconds")
            time.sleep(60)
            gc_group = google_calendar.create_calendar(agu_group_name)
        group_calendar = GroupCalendar.add(gc_group['id'], gc_group['url'], agu_group_id, agu_group_name)
    return group_calendar


def create_all_calendars() -> list[GroupCalendar]:
    agu_api = AguApi()
    groups = agu_api.groups()
    group_calendars = []
    for i, group in enumerate(groups):
        logger.debug("%s/%s" % (i + 1, len(groups)))
        group_id = group['ID']
        group_name = group['SNAME']
        group_calendar = get_or_create_calendars(group_id, group_name)
        group_calendars.append(group_calendar)
    return group_calendars


def add_lessons(lessons: list[Lesson], calendar_id: str):
    group_calendar = GroupCalendar.get_by_google_id(calendar_id)
    google_calendar = AguGoogleCalendar(settings.GOOGLE_SECRET_FILE_PATH)
    for i, lesson in enumerate(lessons):
        logger.debug("%s/%s" % (i + 1, len(lessons)))
        event = google_calendar.add_lesson(
            calendar_id, lesson.time_begin, lesson.time_end, lesson.audience, lesson.groups,
            lesson.name, lesson.discipline_name, lesson.teacher_name, lesson.distant)
        event_id = event['id']
        schedule = Schedule(
            agu_id=lesson.id,
            google_event_id=event_id,
            calendar=group_calendar,
            time_start=lesson.time_begin,
            time_end=lesson.time_end,
            audience=lesson.audience,
            groups=lesson.groups,
            name=lesson.name,
            discipline_name=lesson.discipline_name,
            teacher_name=lesson.teacher_name,
            distant=lesson.distant
        )
        schedule.save()
