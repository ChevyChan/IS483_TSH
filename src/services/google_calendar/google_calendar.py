from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

from pprint import pprint
from Google import Create_Service

from calendar_tasks import *

app = Flask(__name__)
CORS(app)

CLIENT_SECRET_FILE = 'credentials.json'
API_NAME = 'calendar'
API_VERSION='v3'
SCOPES = 'https://www.googleapis.com/auth/calendar'

service = Create_Service(CLIENT_SECRET_FILE, API_NAME, API_VERSION, SCOPES)

def retrievePrimaryCalendar():
  response = service.calendarList().get(calendarId='primary').execute()
  print(response)

def retrieveEventsFromCalendar(calendarId):
  page_token = None
  while True:
    events = service.events().list(calendarId=calendarId, pageToken=page_token).execute()
    for event in events['items']:
      print(event['summary'])
    page_token = events.get('nextPageToken')
    if not page_token:
      break

# Adding events to Google Calendar
def addEventsToCalendar(calendarId):
  # Replace this event details to scheduling details and POST to google calendar and sync with DB to display at Calendar UI
  event = {
    'summary': 'Google I/O 2015',
    'location': '800 Howard St., San Francisco, CA 94103',
    'description': 'A chance to hear more about Google\'s developer products.',
    'start': {
      'dateTime': '2023-12-28T09:00:00-07:00',
      'timeZone': 'Singapore',
    },
    'end': {
      'dateTime': '2023-12-28T17:00:00-07:00',
      'timeZone': 'Singapore',
    }
  }

  event_details = service.events().insert(calendarId=calendarId, body=event).execute()
  print('Event Created: ' + event_details['summary'])

# Updating Events in Google Calendar
def updateEventInCalendar(eventId):
  event = service.events().get(calendarId='primary', eventId=eventId).execute()
  
  event['summary'] = "Delivery to SGH"

  updatedEvent = service.events().update(calendarId='primary', eventId=event['id'], body=event).execute()

  print(updatedEvent)


# Retrieve all tasks from current date onwards and store in the Tasks database
# def pushTasksFromGoogle():
#   tasks_result = Calendar_Tasks.get_list_of_calendars_tasks()
#   print(tasks_result)

addEventsToCalendar('primary')


