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

create_body_details = {
  "status": "needsAction", # Status of the task. This is either "needsAction" or "completed".
  "title": "Setup Virtual Server", # Title of the task.
  "due": "2023-07-21T12:00:00.000Z"
}

def createTaskToCalendar(taskListId, body_details):
  response = service.tasks().insert(tasklist = taskListId, body = body_details).execute()
  print(response)
  return response

def retrieveTasksListFromCalendar():
  page_token = None
  while True:
    tasks = service.tasklists().list(pageToken=page_token).execute()
    for task in tasks['items']:
      print(task)
    page_token = tasks.get('nextPageToken')
    if not page_token:
      break

def retrieveTasks(taskLists):
    tasks = service.tasks().list(tasklist = taskLists, maxResults = 20).execute()
    print(tasks)
  
body_details = {
  "status": "completed"
}

def patchTasks(tasksList, taskId, body_details):
  task_details = service.tasks().patch(tasklist = tasksList, task = taskId, body = body_details).execute()
  print(task_details)


def delete_task(tasksList, taskId):
  task_details = service.tasks().delete(tasklist = tasksList, task = taskId).execute()
  print(task_details)

# All functions are working as expected  
#createTaskToCalendar("MDU2NTM3NTk5NTIwNDUzODE5OTM6MDow", create_body_details)
#retrieveTasksListFromCalendar()
#retrieveTasks("MDU2NTM3NTk5NTIwNDUzODE5OTM6MDow")
#patchTasks("MDU2NTM3NTk5NTIwNDUzODE5OTM6MDow","Vy12TGR4S1cxU3l0WExPMw", body_details)
#delete_task("MDU2NTM3NTk5NTIwNDUzODE5OTM6MDow", "WjhjYVRMalJVbVd2QUVJSg")
