import os
from pprint import pprint

import requests
from requests.models import Response
import pickle

from Google import Create_Service

CLIENT_SECRET_FILE = 'credentials.json'
API_NAME = 'chat'
API_VERSION='v1'
SCOPES = 'https://www.googleapis.com/auth/chat.memberships.app'

service = Create_Service(CLIENT_SECRET_FILE, API_NAME, API_VERSION, SCOPES)

# Create a membership for members
def create_membership(google_spaces, user_name):
    result = service.spaces().members().create(
        # The space in which to create a membership.
        parent = 'spaces/' + google_spaces,

        # Set the Chat app as the entity that gets added to the space.
        # 'app' is an alias for the Chat app calling the API.
        body = {
            'member': {
              'name':'users/' + user_name,
              'type': 'HUMAN'
            }
        }
    ).execute()

    # Prints details about the created membership.
    print(result)

def get_member(member_name):
    # Use the service endpoint to call Chat API.
    result = service.spaces().members().get(

        # The membership to get.
        #
        # Replace SPACE with a space name.
        # Obtain the space name from the spaces resource of Chat API,
        # or from a space's URL.
        #
        # Replace MEMBER with a membership name.
        # Obtain the membership name from the memberships resource of
        # Chat API.
        name='spaces/SPACE/members/'+member_name

    ).execute()

    # Prints details about the created membership.
    print(result)

def retrieve_list_of_members(space_name):
    # Use the service endpoint to call Chat API.
    result = service.spaces().members().list(

        # The space for which to list memberships.
        parent = 'spaces/'+space_name,

        # An OPTIONAL filter that returns only human space members.
        filter = 'member.type = "HUMAN" AND role = "ROLE_MEMBER"'

    ).execute()

    # Prints details about the created membership.
    print(result)