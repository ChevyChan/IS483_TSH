import os.path
import io
from pprint import pprint

import requests
from requests.models import Response
import pickle

from Google import Create_Service
from googleapiclient.http import MediaFileUpload, MediaIoBaseDownload
from urllib.error import HTTPError

CLIENT_SECRET_FILE = 'credentials.json'
API_NAME = 'chat'
API_VERSION='v1'
SCOPES = 'https://www.googleapis.com/auth/chat.spaces https://www.googleapis.com/auth/chat.memberships https://www.googleapis.com/auth/chat.messages'

service = Create_Service(CLIENT_SECRET_FILE, API_NAME, API_VERSION, SCOPES)

# Create a membership for members
def create_spaces(spaces_name):
    '''
    Authenticates with Chat API via user credentials,
    then creates a Chat space.
    '''
    # Use the service endpoint to call Chat API.
    result = service.spaces().create(

      # Details about the space to create.
      body = {

        # To create a named space, set spaceType to SPACE.
        'spaceType': "SPACE",

        # The user-visible name of the space.
        'displayName': spaces_name
      }

      ).execute()

    # Prints details about the created membership.
    print(result)

def create_spaces_with_members(spaces_name, **members):
    # Use the service endpoint to call Chat API.
    result = service.spaces().setup(

      # Details about the space to set up.
      body = {

        # Attributes of the space to set up, like space type and display name.
        'space': {

            # To set up a named space, set spaceType to SPACE.
            'spaceType': 'SPACE',

            # The user-visible name of the space
            'displayName': spaces_name
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


# Functions for Google Membership
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

# Functions for Google Spaces
def create_messages(spaces_name, body_text, upload_file):
    if(upload_file != ""):
        try:
            # Check for file extension of the upload_file
            file_ext = upload_file.split('.')[1]

            # Upload a file to Google Chat.
            media = MediaFileUpload(upload_file, mimetype='image/'+file_ext)

            # Create a message and attach the uploaded file to it.
            attachment_uploaded = service.media().upload(

                # The space to upload the attachment in.
                #
                # Replace SPACE with a space name.
                # Obtain the space name from the spaces resource of Chat API,
                # or from a space's URL.
                parent='spaces/' + spaces_name,

                # The filename of the attachment, including the file extension.
                body={'filename': upload_file},

                # Media resource of the attachment.
                media_body=media

            ).execute()

            print(attachment_uploaded)

            # Create a Chat message with attachment.
            result = service.spaces().messages().create(
                # The space to create the message in.
                #
                # Replace SPACE with a space name.
                # Obtain the space name from the spaces resource of Chat API,
                # or from a space's URL.
                #
                # Must match the space name that the attachment is uploaded to.
                parent='spaces/'+spaces_name,

                # The message to create.
                body={
                    'text': body_text,
                    'attachment': [attachment_uploaded]
                }

            ).execute()

            print(result)
            return result
        except HTTPError as err:
            print(err)
    else:
        try:
            # Create a Chat message if no attachment.
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
            return result
        except HTTPError as err:
            print(err)

# Get messages and attachments (if any) by caching into DB first and then, retrieve message from DB
def get_messages(spaces_name):
    response = create_messages('AAAAouZ1mcE', "Annyeong World!", "")
    if('attachment' in response):
        # Get a Chat message.
        result = service.spaces().messages().attachments().get(

            # The message to get.
            #
            # Replace SPACE with a space name.
            # Obtain the space name from the spaces resource of Chat API,
            # or from a space's URL.
            #
            # Replace MESSAGE with a message name.
            # Obtain the message name from the response body returned
            # after creating a message asynchronously with Chat REST API.
            name='spaces/' + spaces_name + '/messages/' + response["name"].slice("/")[3] + '/attachments/' + response["attachment"]

        ).execute()

        # Print Chat API's response in your command line interface.
        print(result)
    else:
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
            name = 'spaces/' + spaces_name + '/messages/' + response["name"].split("/")[3]

        ).execute()

        # Prints details about the created membership.
        print(result)

def get_list_messages(spaces_name):
    # Use the service endpoint to call Chat API.
    result = service.spaces().messages().list(

          # The space for which to list messages.
          parent = 'spaces/'+spaces_name,

          # An optional filter that returns messages
          # created after March 16, 2023.
          # filter = 'createTime > ' + filter_date_time
          orderBy = "createTime ASC" 

      ).execute()

    # Prints details about the created membership.
    print(result)

def download_attachment(RESOURCE_NAME):
    # Download media resource.
    request = service.media().download_media(
        resourceName=RESOURCE_NAME,
    )
    file = io.BytesIO()
    downloader = MediaIoBaseDownload(file, request)

    done = False
    while done is False:
        status, done = downloader.next_chunk()
        if status.total_size:
            print(f'Total size: {status.total_size}')
        print(f'Download {int(status.progress() * 100)}')


# create_messages('AAAAouZ1mcE', "Hello World!", "")

# get_messages('AAAAouZ1mcE')

get_list_messages('AAAAouZ1mcE')

#create_spaces("IS483_TSH_Group1")