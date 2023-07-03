from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

from pprint import pprint
from Google import Create_Service

app = Flask(__name__)
CORS(app)

CLIENT_SECRET_FILE = 'credentials.json'
API_NAME = 'calendar'
API_VERSION='v3'
SCOPES = 'https://www.googleapis.com/auth/calendar'

service = Create_Service(CLIENT_SECRET_FILE, API_NAME, API_VERSION, SCOPES)

response = service.calendars().get(calendarId='primary').execute()
print(response)