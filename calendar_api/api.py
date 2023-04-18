from datetime import datetime

from google.oauth2 import service_account
from googleapiclient.discovery import build


class GoogleCalendar:
    SCOPES = ['https://www.googleapis.com/auth/calendar']

    def __init__(self, file_path: str):
        credentials = service_account.Credentials.from_service_account_file(
            filename=file_path, scopes=self.SCOPES
        )
        self.service = build('calendar', 'v3', credentials=credentials)

    def get_calendar_list(self):
        return self.service.calendarList().list().execute()

    def add_calendar(self, name):
        new_calendar = {
            'summary': name,
            'timeZone': 'Asia/Novosibirsk'
        }
        return self.service.calendars().insert(body=new_calendar).execute()

    def add_event(self, calendar_id, event):
        return self.service.events().insert(
            calendarId=calendar_id,
            body=event).execute()

    def delete_event(self, calendar_id, event_id):
        return self.service.events().delete(
            calendarId=calendar_id,
            eventId=event_id).execute()

    def add_rule(self, calendar_id):
        rule = {
            'scope': {
                'type': 'default',
            },
            'role': 'reader'
        }
        return self.service.acl().insert(calendarId=calendar_id, body=rule).execute()

    def create_calendar(self, name):
        calendar = self.add_calendar(name)
        calendar_id = calendar['id']
        self.add_rule(calendar_id)
        calendar_link = f'https://calendar.google.com/calendar/r?cid={calendar_id}'
        obj = {
            'id': calendar_id,
            'url': calendar_link,
        }
        return obj

    def get_colors(self):
        return self.service.colors().get().execute()


class AguGoogleCalendar(GoogleCalendar):
    def add_lesson(self, calendar_id: str, time_begin: datetime, time_end: datetime, audience: str, groups: list[str],
                   name: str, discipline_name: str, teacher_name: str, distant: bool = False):
        time_begin = time_begin.strftime("%Y-%m-%dT%H:%M:%S")
        time_end = time_end.strftime("%Y-%m-%dT%H:%M:%S")

        description = f"{name}\n" \
                      f"Группы:\n"
        for i, group in enumerate(groups):
            description += f"{i + 1}. {group}\n"

        description += f"{teacher_name}"

        event = {
            'summary': discipline_name,
            'location': audience,
            'description': description,
            'start': {
                'dateTime': time_begin,
                'timeZone': 'Asia/Novosibirsk',
            },
            'end': {
                'dateTime': time_end,
                'timeZone': 'Asia/Novosibirsk',
            },
            # 'colorId': '9'
        }

        event = self.add_event(calendar_id=calendar_id, event=event)
        return event
