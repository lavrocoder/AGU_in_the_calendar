class Updater:
    @classmethod
    def get_schedule(cls):
        """
        Получает расписание из API агу
        :return:
        """
        pass

    @classmethod
    def get_changes(cls, schedule):
        """
        Получает изменения на основе полученного расписания и данных в базе данных.
        :param schedule: Расписание полученное методом get_schedule.
        :return:
        """
        pass

    @classmethod
    def update_calendar(cls, changes):
        """
        Обновляет гугл календарь на основе изменений расписания.
        :param changes: Изменения расписания, полученные методом get_changes.
        :return:
        """
        pass
