import os.path
import datetime
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
import pickle

# If modifying scopes, delete token.pickle
SCOPES = ['https://www.googleapis.com/auth/calendar',
          'https://www.googleapis.com/auth/gmail.readonly']

def get_credentials():
    creds = None

    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)

        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    return creds
def get_calendar_service():
    creds = get_credentials()
    service = build('calendar', 'v3', credentials=creds)
    return service
def get_gmail_service():
    creds = get_credentials()
    service = build('gmail', 'v1', credentials=creds)
    return service

def get_unread_emails():
    service = get_gmail_service()

    results = service.users().messages().list(
        userId='me',
        labelIds=['UNREAD'],
        maxResults=5
    ).execute()

    messages = results.get('messages', [])

    emails = []

    for msg in messages:
        msg_data = service.users().messages().get(
            userId='me',
            id=msg['id']
        ).execute()

        headers = msg_data['payload']['headers']

        sender = ""
        subject = ""

        for header in headers:
            if header['name'] == 'From':
                sender = header['value']
            if header['name'] == 'Subject':
                subject = header['value']

        snippet = msg_data.get('snippet', '')

        emails.append({
            "id": msg['id'],
            "sender": sender,
            "subject": subject,
            "body": snippet
        })

    return emails
def mark_as_read(message_id):
    service = get_gmail_service()

    service.users().messages().modify(
        userId='me',
        id=message_id,
        body={'removeLabelIds': ['UNREAD']}
    ).execute()



def create_event(summary, start_time, end_time):
    service = get_calendar_service()

    event = {
        'summary': summary,
        'start': {
            'dateTime': start_time.isoformat(),
            'timeZone': 'Asia/Kolkata',  # change if needed
        },
        'end': {
            'dateTime': end_time.isoformat(),
            'timeZone': 'Asia/Kolkata',
        },
    }

    event = service.events().insert(calendarId='primary', body=event).execute()

    print("✅ Event created:", event.get('htmlLink'))
    return event.get('id')

def delete_event(google_event_id):
    service = get_calendar_service()

    service.events().delete(
        calendarId='primary',
        eventId=google_event_id
    ).execute()

    print("🗑 Old event deleted from Google Calendar")
