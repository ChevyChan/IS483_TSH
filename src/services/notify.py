#!/usr/bin/env python3
# The above shebang (#!) operator tells Unix-like environments
# to run this file as a python3 script

import json
import os

import amqp_setup
import os
from twilio.rest import Client

import email
import smtplib
import ssl

from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

monitorBindingKey = '*.notify'


def receiveReportLog():
    amqp_setup.check_setup()

    queue_name = 'Notify'

    # set up a consumer and start to wait for coming messages
    amqp_setup.channel.basic_consume(
        queue=queue_name, on_message_callback=callback, auto_ack=True)
    # an implicit loop waiting to receive messages;
    amqp_setup.channel.start_consuming()
    # it doesn't exit by default. Use Ctrl+C in the command window to terminate it.


# required signature for the callback; no return
def callback(channel, method, properties, body):
    print("\nReceived an sms log")
    # processReportLog(json.loads(body))

    # processSMS()
    processemail()
    print("SMSSSSS/ Email SENTTTTT")  # print a new line feed

    print("\nReceived an report log by " + __file__)
    processnotify(json.loads(body))
    print()  # print a new line feed


# def processSMS():
#     print("Sending an sms")
#     account_sid = "AC94cbf138c93df61491a51bb6d6782d7b"
#     auth_token = "0cd5fa293cc5c029a565ce0227d54b65"
#     client = Client(account_sid, auth_token)

#     message = client.messages.create(
#         body="You have recently allowed access. View approved list for more details",
#         from_="+12766336073",
#         to="+6581919797"
#     )

#     print(message.sid)


def processnotify(thenotify):
    print("Recording log:")
    print(thenotify)


def processemail():
    subject = "Recent allowed access"
    body = "You have receive a notification."
    sender_email = "swinnertonpok@gmail.com"
    receiver_email = "pokjingkai@gmail.com"
    password = "xvjpzkvrsbwwcynz"

    # Create a multipart message and set headers
    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = receiver_email
    message["Subject"] = subject
    message["Bcc"] = receiver_email  # Recommended for mass emails

    # Add body to email
    message.attach(MIMEText(body, "plain"))

    # In same directory as script

    text = message.as_string()

    # Log in to server using secure context and send email
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, text)


# execute this program only if it is run as a script (not by 'import')
if __name__ == "__main__":
    # print("\nThis is " + os.path.basename(__file__), end='')
    print(": monitoring routing key '{}' in exchange '{}' ...".format(
        monitorBindingKey, amqp_setup.exchangename))
    receiveReportLog()
