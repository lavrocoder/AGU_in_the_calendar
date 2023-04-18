import datetime

from django.conf import settings
from django.core.management import BaseCommand

from agu_api.api import AguApi
from calendar_api.api import GoogleCalendar
from .schedule_updater_module import Updater
from ...models import GroupCalendar


def main():
    agu_api = AguApi()
    groups = agu_api.groups()
    for agu_group in groups:
        group_id = agu_group['ID']
        bd_group = GroupCalendar.get_by_agu_id(group_id)
        if bd_group is None:
            group_name = agu_group['SNAME']
            google_calendar = GoogleCalendar(settings.GOOGLE_SECRET_FILE_PATH)
            gc_group = google_calendar.create_calendar(group_name)
            bd_group = GroupCalendar.add(gc_group['id'], gc_group['url'], group_id, group_name)

        today = datetime.datetime.now()
        today = today.strftime("%d.%m.%Y")
        timetable = agu_api.timetable(today, 3, 3, bd_group.agu_id)

        print(timetable)


class Command(BaseCommand):
    help = "Программа обновления расписания"

    def handle(self, *args, **options):
        main()
