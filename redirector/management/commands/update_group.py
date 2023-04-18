from django.core.management import BaseCommand

from agu_api import Agu
from .schedule_updater_module.utils import get_or_create_calendars, add_lessons


def main():
    group_id = '4319'
    group_name = '1225и'

    group_calendar = get_or_create_calendars(group_id, group_name)

    agu = Agu()
    lessons = agu.get_timetable_for_group_for_month(group_id)
    add_lessons(lessons, group_calendar.google_id)


class Command(BaseCommand):
    help = "Обновляет расписание для группы по её id"

    def handle(self, *args, **options):
        main()
