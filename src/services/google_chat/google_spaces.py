import os
from pprint import pprint

import requests
from requests.models import Response
import pickle

from Google import Create_Service

CLIENT_SECRET_FILE = 'credentials.json'
API_NAME = 'chat'
API_VERSION='v1'
SCOPES = 'https://www.googleapis.com/auth/chat.spaces.create'

service = Create_Service(CLIENT_SECRET_FILE, API_NAME, API_VERSION, SCOPES)

# Create a membership for members
def create_spaces(google_spaces):
    '''
    Authenticates with Chat API via user credentials,
    then creates a Chat space.
    '''
    # Use the service endpoint to call Chat API.
    result = service.spaces().create(

      # Details about the space to create.
      body = {

        # To create a named space, set spaceType to SPACE.
        'spaceType': google_spaces,

        # The user-visible name of the space.
        'displayName': 'API-made'
      }

      ).execute()

    # Prints details about the created membership.
    print(result)

def create_spaces_with_members(google_spaces, **members):
    # Use the service endpoint to call Chat API.
    result = service.spaces().setup(

      # Details about the space to set up.
      body = {

        # Attributes of the space to set up, like space type and display name.
        'space': {

            # To set up a named space, set spaceType to SPACE.
            'spaceType': google_spaces,

            # The user-visible name of the space
            'displayName': 'API-setup'
        },

        # The people and app to add to the space.
        #
        # The authenticated user is automatically added to the space,
        # and doesn't need to be specified in the memberships array.
        'memberships': [
            {
              'member': {
                'name':'users/'+members,
                'type': 'HUMAN'
              }
            },
            {
              'member': {
                'name':'users/'+members,
                'type': 'HUMAN'
              }
            }
        ]
      }

      ).execute()

    # Prints details about the created membership.
    print(result)

def retrieve_spaces(spaces_name):
    # Use the service endpoint to call Chat API.
    result = service.spaces().get(

          # The space to get.
          #
          # Replace SPACE with a space name.
          # Obtain the space name from the spaces resource of Chat API,
          # or from a space's URL.
          name='spaces/'+spaces_name

      ).execute()

    # Prints details about the space.
    print(result)

def retrieve_all_spaces():
    # Use the service endpoint to call Chat API.
    result = service.spaces().list(

          # An OPTIONAL filter that returns named spaces or unnamed group chats,
          # but not direct messages (DMs).
          # Can be used for search filtering
          filter='spaceType = "SPACE" OR spaceType = "GROUP_CHAT"'

      ).execute()

    # Prints the returned list of spaces.
    print(result)

def delete_selected_spaces(google_spaces):
     # Use the service endpoint to call Chat API.
    result = service.spaces().delete(

          # The space to delete.
          #
          # Replace SPACE with a space name.
          # Obtain the space name from the spaces resource of Chat API,
          # or from a space's URL.
          name='spaces/'+google_spaces

      ).execute()

    # Print Chat API's response in your command line interface.
    # When deleting a space, the response body is empty.
    print(result)


if __name__ == '__main__':
    create_spaces("My Space")