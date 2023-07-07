import os.path
import io
from pprint import pprint

import requests
from requests.models import Response
import pickle

from googleapiclient.http import MediaFileUpload, MediaIoBaseDownload

from Google import Create_Service

CLIENT_SECRET_FILE = 'credentials.json'
API_NAME = 'chat'
API_VERSION='v1'
SCOPES = 'https://www.googleapis.com/auth/chat.messages.create'

service = Create_Service(CLIENT_SECRET_FILE, API_NAME, API_VERSION, SCOPES)

# def upload_documents(space_name, body_text, upload_file):
#     # Check for file extension of the upload_file
#     file_ext = upload_file.split('.')[1]

#     # Upload a file to Google Chat.
#     media = MediaFileUpload(upload_file, mimetype='image/'+file_ext)

#     # Create a message and attach the uploaded file to it.
#     attachment_uploaded = service.media().upload(

#         # The space to upload the attachment in.
#         #
#         # Replace SPACE with a space name.
#         # Obtain the space name from the spaces resource of Chat API,
#         # or from a space's URL.
#         parent='spaces/' + space_name,

#         # The filename of the attachment, including the file extension.
#         body={'filename': upload_file},

#         # Media resource of the attachment.
#         media_body=media

#     ).execute()

#     print(attachment_uploaded)

#     # Create a Chat message with attachment.
#     result = service.spaces().messages().create(

#         # The space to create the message in.
#         #
#         # Replace SPACE with a space name.
#         # Obtain the space name from the spaces resource of Chat API,
#         # or from a space's URL.
#         #
#         # Must match the space name that the attachment is uploaded to.
#         parent='spaces/'+space_name,

#         # The message to create.
#         body={
#             'text': body_text,
#             'attachment': [attachment_uploaded]
#         }

#     ).execute()

#     print(result)

# def get_attachment(space_name):
#     # Get a Chat message.
#     result = service.spaces().messages().attachments().get(

#         # The message to get.
#         #
#         # Replace SPACE with a space name.
#         # Obtain the space name from the spaces resource of Chat API,
#         # or from a space's URL.
#         #
#         # Replace MESSAGE with a message name.
#         # Obtain the message name from the response body returned
#         # after creating a message asynchronously with Chat REST API.
#         name='spaces/' + space_name + '/messages/MESSAGE/attachments/ATTACHMENT'

#     ).execute()

#     # Print Chat API's response in your command line interface.
#     print(result)

# def download_attachment(RESOURCE_NAME):
#     # Download media resource.
#     request = service.media().download_media(
#         resourceName=RESOURCE_NAME,
#     )
#     file = io.BytesIO()
#     downloader = MediaIoBaseDownload(file, request)

#     done = False
#     while done is False:
#         status, done = downloader.next_chunk()
#         if status.total_size:
#             print(f'Total size: {status.total_size}')
#         print(f'Download {int(status.progress() * 100)}')

