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
SCOPES = 'https://www.googleapis.com/auth/chat.messages'

service = Create_Service(CLIENT_SECRET_FILE, API_NAME, API_VERSION, SCOPES)

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
def get_messages(spaces_name, body_text, body_attachment):
    if(body_attachment != ""):
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
            name='spaces/' + spaces_name + '/messages/' + body_text + '/attachments/' + body_attachment

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


create_messages('AAAAouZ1mcE', "Hello World!", "")