from django.core.management import BaseCommand

from .schedule_updater_module import Updater


def main():
    schedule = Updater.get_schedule()
    changes = Updater.get_changes(schedule)
    Updater.update_calendar(changes)


class Command(BaseCommand):
    help = "Программа обновления расписания"

    def handle(self, *args, **options):
        main()
