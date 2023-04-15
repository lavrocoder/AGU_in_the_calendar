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
