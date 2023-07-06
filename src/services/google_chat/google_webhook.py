"""A sample to send message on Google Chat group with Python requests.
Prerequisites:
- Google API v1
- A webhook URL taken
Usage:
```bash
WEBHOOK_URL='https://chat.googleapis.com/v1/spaces/AAAAdOUcFZM/messages?key=&token=xxx' 
```
Ref:
- https://developers.google.com/hangouts/chat/quickstart/incoming-bot-python
- https://developers.google.com/hangouts/chat/reference/message-formats
"""

import os
from pprint import pprint

import requests
from requests.models import Response
import pickle

result = pickle.load(open("./token files/token_calendar_v3.pickle","rb"))
print(result.token)

# You need to pass WEBHOOK_URL as an environment variable.
os.environ['WEBHOOK_URL'] = 'https://chat.googleapis.com/v1/spaces/AAAAdOUcFZM/messages?key=AIzaSyCeJEuM7GE3kTwgZda9ppRZjLxcDreNXIY&token='+result.token
WEBHOOK_URL = os.environ['WEBHOOK_URL']

def main():
    # res = send_text(text='Hello!')
    res = send_text_card(
        text='Hey!',
        subtitle='You!',
        paragraph='<b>Roses</b> are <font color=\"#ff0000\">red</font>,<br><i>Violets</i> are <font color=\"#0000ff\">blue</font>',
    )
    pprint(res.json())
    pass


def send_text(text: str) -> Response:
    return requests.post(WEBHOOK_URL, json={'text': text})


def send_text_card(title: str, subtitle: str, paragraph: str) -> Response:
    header = {
        'title': title,
        'subtitle': subtitle,
    }
    widget = {'textParagraph': {'text': paragraph}}
    return requests.post(
        WEBHOOK_URL,
        json={
            'cards': [
                {
                    'header': header,
                    'sections': [{'widgets': [widget]}],
                }
            ]
        },
    )


if __name__ == '__main__':
    main()
