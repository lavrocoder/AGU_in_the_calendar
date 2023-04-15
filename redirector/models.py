from django.db import models


class Schedule(models.Model):
    agu_id = models.CharField(max_length=250)
    discipline_name = models.CharField(max_length=250)
    type = models.CharField(max_length=250)
    distant = models.BooleanField(default=False)
    place = models.CharField(max_length=250)
    time_start = models.TimeField()
    time_end = models.TimeField()
    teacher = models.CharField(max_length=250)


class GroupCalendar(models.Model):
    google_id = models.CharField(max_length=250)
    url = models.CharField(max_length=250)
    agu_id = models.CharField(max_length=250)
    group = models.CharField(max_length=250)
