from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

from pprint import pprint
from Google import Create_Service
import socket

from calendar_tasks import *

app = Flask(__name__)
CORS(app)

CLIENT_SECRET_FILE = 'credentials.json'
API_NAME = 'calendar'
API_VERSION='v3'
SCOPES = 'https://www.googleapis.com/auth/calendar'

service = Create_Service(CLIENT_SECRET_FILE, API_NAME, API_VERSION, SCOPES)

socket.setdefaulttimeout(10000)

@app.route("/v1/google_calendar/retrieve_default_calendar")
def retrievePrimaryCalendar():
  response = service.calendarList().get(calendarId='primary').execute()
  print(response)
  return response

@app.route("/v1/google_calendar/retrieve_calendar_events/<string:calendarId>")
def retrieveEventsFromCalendar(calendarId):
  page_token = None
  while True:
    events = service.events().list(calendarId=calendarId, pageToken=page_token, timeMin='2023-05-01T00:00:00-07:00', timeMax='2023-12-31T23:59:00-23:59').execute()
    for event in events['items']:
      print(event['summary'])
      return event
    page_token = events.get('nextPageToken')
    if not page_token:
      break

@app.route("/v1/google_calendar/create_calendar_events/<string:calendarId>/<string:summary>/<string:location>/<string:description>/<string:startTime>/<string:endTime>", methods=['POST'])
# Adding events to Google Calendar
def addEventsToCalendar(calendarId, summary, location, description, startTime, endTime):
  # Replace this event details to scheduling details and POST to google calendar and sync with DB to display at Calendar UI
  # events_result = retrieveEventsFromCalendar(calendarId)
  event = {
    'summary': summary,
    'location': location,
    'description': description,
    'start': {
      'dateTime': startTime,
      'timeZone': 'Singapore',
    },
    'end': {
      'dateTime': endTime,
      'timeZone': 'Singapore',
    }
  }

  event_details = service.events().insert(calendarId=calendarId, body=event).execute()
  print('Event Created: ' + event_details['summary'])
  return 'Event Created: ' + event_details['summary']

@app.route("/v1/google_calendar/update_calendar_event", methods=['PUT'])
# Updating Events in Google Calendar
def updateEventInCalendar(eventId):
  event = service.events().get(calendarId='primary', eventId=eventId).execute()
  
  event['summary'] = "Delivery to SGH"

  updatedEvent = service.events().update(calendarId='primary', eventId=event['id'], body=event).execute()

  print(updatedEvent)
  return updatedEvent


# Retrieve all tasks from current date onwards and store in the Tasks database
# def pushTasksFromGoogle():
#   tasks_result = Calendar_Tasks.get_list_of_calendars_tasks()
#   print(tasks_result)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5002, debug=True)
    #retrievePrimaryCalendar()
    #addEventsToCalendar("chevychan1@gmail.com", "Delivery to TSH", "Sims Ave", "Test Delivery", "2023-06-28T16:35:36-16:35", "2023-06-28T16:35:36-16:35")
