from django.contrib import admin

from redirector.models import Lesson


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ('id', 'type', 'value', 'lesson_id', 'time_start', 'time_end', 'hash')
    list_display_links = ('id', 'type', 'value', 'lesson_id', 'time_start', 'time_end', 'hash')
    search_fields = ('id', 'type', 'value', 'lesson_id', 'time_start', 'time_end', 'hash')
