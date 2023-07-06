import os
from pprint import pprint

import requests
from requests.models import Response
import pickle

from Google import Create_Service

CLIENT_SECRET_FILE = 'credentials.json'
API_NAME = 'chat'
API_VERSION='v1'
SCOPES = 'https://www.googleapis.com/auth/chat.messages.create'

service = Create_Service(CLIENT_SECRET_FILE, API_NAME, API_VERSION, SCOPES)

def create_messages(spaces_name, body_text):
    # Create a Chat message.
    result = service.spaces().messages().create(

    # The space to create the message in.
    #
    # Replace SPACE with a space name.
    # Obtain the space name from the spaces resource of Chat API,
    # or from a space's URL.
    parent='spaces/'+spaces_name,

    # The message to create.
    body={'text': body_text}

    ).execute()

    print(result)

def get_messages(spaces_name, body_text):
    # Use the service endpoint to call Chat API.
    result = service.spaces().messages().get(

        # The message to get.
        #
        # Replace SPACE with a space name.
        # Obtain the space name from the spaces resource of Chat API,
        # or from a space's URL.
        #
        # Replace MESSAGE with a message name.
        # Obtain the message name from the response body returned
        # after creating a message asynchronously with Chat REST API.
        name = 'spaces/' + spaces_name + '/messages/' + body_text

    ).execute()

    # Prints details about the created membership.
    print(result)

def get_list_messages(spaces_name, filter_date_time):
    # Use the service endpoint to call Chat API.
    result = service.spaces().messages().list(

          # The space for which to list messages.
          parent = 'spaces/'+spaces_name,

          # An optional filter that returns messages
          # created after March 16, 2023.
          filter = 'createTime > ' + filter_date_time 

      ).execute()

    # Prints details about the created membership.
    print(result)