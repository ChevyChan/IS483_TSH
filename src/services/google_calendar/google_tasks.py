from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

from pprint import pprint
from Google import Create_Service

from calendar_tasks import *

app = Flask(__name__)
CORS(app)

CLIENT_SECRET_FILE = 'credentials.json'
API_NAME = 'tasks'
API_VERSION='v1'
SCOPES = 'https://www.googleapis.com/auth/tasks'

service = Create_Service(CLIENT_SECRET_FILE, API_NAME, API_VERSION, SCOPES)

def retrieveTasksListFromCalendar():
  page_token = None
  while True:
    tasks = service.tasklists().list(pageToken=page_token).execute()
    for task in tasks['items']:
      print(task)
    page_token = tasks.get('nextPageToken')
    if not page_token:
      break

def retrieveTasks():
    tasks = service.tasklists().get(tasklist='MDU2NTM3NTk5NTIwNDUzODE5OTM6MDow').execute()
    print(tasks)


#retrieveTasksListFromCalendar()
retrieveTasks()