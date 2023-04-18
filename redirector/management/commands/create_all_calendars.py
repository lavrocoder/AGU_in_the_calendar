from django.core.management import BaseCommand

from .schedule_updater_module.utils import create_all_calendars


def main():
    calendars = create_all_calendars()
    print(calendars)


class Command(BaseCommand):
    help = "Создает все календари из API АГУ"

    def handle(self, *args, **options):
        main()
