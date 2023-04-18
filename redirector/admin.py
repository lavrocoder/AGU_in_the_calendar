from django.contrib import admin

from redirector.models import GroupCalendar
# from redirector.models import Schedule


# @admin.register(Schedule)
# class ScheduleAdmin(admin.ModelAdmin):
#     list_display = ("google_id", "discipline_name", "groups", "type", "distant", "place", "time_start", "time_end", "teacher")
#     list_display_links = ("google_id", "discipline_name", "groups", "type", "distant", "place", "time_start", "time_end", "teacher")
#     search_fields = ("google_id", "discipline_name", "groups", "type", "distant", "place", "time_start", "time_end", "teacher")


@admin.register(GroupCalendar)
class GroupCalendarAdmin(admin.ModelAdmin):
    list_display = ("google_id", "url", "google_id", "group")
    list_display_links = ("google_id", "url", "google_id", "group")
    search_fields = ("google_id", "url", "google_id", "group")
