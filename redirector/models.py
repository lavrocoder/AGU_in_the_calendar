from __future__ import annotations

from django import forms
from django.db import models


class GroupCalendar(models.Model):
    google_id = models.CharField(max_length=250, unique=True)
    url = models.CharField(max_length=250, unique=True)
    agu_id = models.CharField(max_length=250, unique=True)
    group = models.CharField(max_length=250)

    @classmethod
    def get_by_agu_id(cls, agu_id) -> GroupCalendar | None:
        """
        Получает объект календаря группы по google_id.
        :param agu_id: Уникальный ID группы из API АГУ.
        :return: Объект GroupCalendar | None если календарь не найден или их больше 1.
        """
        try:
            calendar = cls.objects.get(agu_id=agu_id)
        except (cls.MultipleObjectsReturned, cls.DoesNotExist):
            calendar = None
        return calendar

    @classmethod
    def get_by_google_id(cls, google_id) -> GroupCalendar | None:
        """
        Получает объект календаря группы по id календаря.
        :param google_id: Уникальный ID календаря.
        :return: Объект GroupCalendar | None если календарь не найден или их больше 1.
        """
        try:
            calendar = cls.objects.get(google_id=google_id)
        except (cls.MultipleObjectsReturned, cls.DoesNotExist):
            calendar = None
        return calendar

    @classmethod
    def add(cls, google_id, url, agu_id, group_name) -> GroupCalendar:
        """
        Добавляет календарь в базу данных.
        :param google_id: ID календаря в Google.
        :param url: Ссылка на Google календарь.
        :param agu_id: ID группы в АГУ API.
        :param group_name: Название группы
        :return:
        """
        calendar = cls(google_id=google_id, url=url, agu_id=agu_id, group=group_name)
        calendar.save()
        return calendar


class ListField(models.TextField):

    def __init__(self, *args, **kwargs):
        self.delimiter = kwargs.pop('delimiter', ',')
        super().__init__(*args, **kwargs)

    def to_python(self, value):
        if isinstance(value, list):
            return value

        if value is None:
            return []

        return value.split(self.delimiter)

    def get_prep_value(self, value):
        if not value:
            return ''

        return self.delimiter.join(str(s) for s in value)

    def value_to_string(self, obj):
        value = self.value_from_object(obj)
        return self.get_prep_value(value)

    def formfield(self, **kwargs):
        defaults = {
            'widget': forms.Textarea(attrs={'rows': 3}),
            'help_text': 'Enter values separated by commas',
        }
        defaults.update(kwargs)
        return super().formfield(**defaults)


class Schedule(models.Model):
    agu_id = models.CharField(max_length=250)
    google_event_id = models.CharField(max_length=250)
    calendar = models.ForeignKey(GroupCalendar, models.CASCADE)
    time_start = models.TimeField()
    time_end = models.TimeField()
    audience = models.CharField(max_length=250)
    groups = ListField()
    name = models.CharField(max_length=250)
    discipline_name = models.CharField(max_length=250)
    teacher_name = models.CharField(max_length=250)
    distant = models.BooleanField(default=False)

    @classmethod
    def get_by_agu_id(cls, agu_id: str):
        """
        Получает объект календаря группы по google_id.
        :param agu_id: Уникальный ID группы из API АГУ.
        :return: Объект GroupCalendar | None если календарь не найден или их больше 1.
        """
        try:
            lesson = cls.objects.get(agu_id=agu_id)
        except (cls.MultipleObjectsReturned, cls.DoesNotExist):
            lesson = None
        return lesson
