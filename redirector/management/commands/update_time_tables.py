import os

import pytz
from django.conf import settings
from django.core.management import BaseCommand
from django.utils.timezone import make_aware
from loguru import logger

from agu_api import Agu
from ical import Ical
from redirector.models import Lesson
from redirector.management.commands.utils import get_first_day_of_current_month_and_last_day_of_next_month


def main():
    log_path = os.path.join(
        settings.BASE_DIR, 'logs', 'update_time_tables_{time}.log'
    )
    logger.add(log_path)

    timezone = pytz.timezone(settings.TIME_ZONE)

    date_start, date_end = get_first_day_of_current_month_and_last_day_of_next_month()
    agu = Agu()

    for lesson_type in range(3):
        lesson_type += 1
        groups_or_teachers_or_auditoriums = agu.get_id_sname(lesson_type)

        for i, item in enumerate(groups_or_teachers_or_auditoriums):
            logger.debug("%s/%s %s" % (i + 1, len(groups_or_teachers_or_auditoriums), item))
            value = item.ID
            lessons = agu.get_lessons_for_current_2_month(lesson_type, value)

            # Создание календаря
            ical_path = os.path.join(settings.BASE_DIR, "static", "calendars", f"type_{lesson_type}_value_{value}.ics")
            if not os.path.exists(ical_path):
                Ical.create_calendar(ical_path, item.SNAME)

            # Загрузка Ical
            ical_calendar = Ical.from_file(ical_path)

            db_lessons_to_save = []
            # Добавление и обновление событий
            for lesson in lessons:
                lesson_hash = lesson.hash()
                uid = f"type_{lesson_type}_value_{value}_id_{lesson.id}@rb.asu.ru"
                try:
                    db_lesson = Lesson.objects.get(type=lesson_type, value=value, lesson_id=lesson.id)
                except Lesson.DoesNotExist:
                    # Добавление занятия в базу данных
                    logger.debug("Add %s" % lesson)
                    # Здесь код обновления данных в гугл и ical

                    # Ical
                    ical_calendar = Ical.add_lesson(lesson, ical_calendar, uid)

                    db_lesson = Lesson(type=lesson_type, value=value, lesson_id=lesson.id,
                                       time_start=make_aware(lesson.time_begin, timezone),
                                       time_end=make_aware(lesson.time_end, timezone), hash=lesson_hash)
                    db_lessons_to_save.append(db_lesson)
                else:
                    if db_lesson.hash != lesson_hash:
                        # Изменение занятия в базе данных
                        logger.debug("Update %s" % lesson)
                        # Здесь код обновления данных в гугл и ical

                        # Ical
                        Ical.edit_lesson(lesson, ical_calendar, uid)
                        # ...
                        # ...
                        db_lesson.hash = lesson_hash
                        db_lesson.time_start = make_aware(lesson.time_begin, timezone)
                        db_lesson.time_end = make_aware(lesson.time_end, timezone)
                        db_lessons_to_save.append(db_lesson)

            # Удаление данных
            db_lessons = Lesson.get_by_interval(make_aware(date_start, timezone), make_aware(date_end, timezone),
                                                lesson_type, value)
            for db_lesson in db_lessons:
                if db_lesson.lesson_id not in [lesson.id for lesson in lessons]:
                    logger.debug("Remove %s" % db_lesson)
                    # Здесь код удаления данных из гугл и ical

                    # Ical
                    uid = f"type_{lesson_type}_value_{value}_id_{db_lesson.lesson_id}@rb.asu.ru"
                    Ical.delete_lesson(ical_calendar, uid)
                    # ...
                    # ...
                    db_lesson.delete()

            Ical.save(ical_path, ical_calendar)

            for db_lesson_to_save in db_lessons_to_save:
                db_lesson_to_save.save()


class Command(BaseCommand):
    help = "Обновляет расписание"

    def handle(self, *args, **options):
        main()
