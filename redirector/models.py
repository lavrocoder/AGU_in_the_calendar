from __future__ import annotations

from datetime import datetime

from django.db import models
from django.http import QueryDict


class Lesson(models.Model):
    type = models.CharField(
        max_length=250,
        verbose_name="Тип расписания",
        help_text="1 - для преподавателей, 2 - для аудитории, 3 - для студентов"
    )
    value = models.CharField(
        max_length=250,
        verbose_name="Идентификатор",
        help_text="Идентификатор преподавателя, аудитории или группы"
    )
    lesson_id = models.CharField(max_length=250, verbose_name="ID пары")
    time_start = models.DateTimeField()
    time_end = models.DateTimeField()
    hash = models.CharField(max_length=250, verbose_name="Хэш", help_text="Хэш пары")

    @classmethod
    def get_by_interval(cls, date_start: datetime, date_end: datetime, lesson_type: str | int,
                        value: str) -> QueryDict[Lesson]:
        return cls.objects.filter(type=lesson_type, value=value, time_start__gte=date_start, time_start__lte=date_end)
