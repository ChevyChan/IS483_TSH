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

monitorBindingKey = '*.error'


def receiveOrderLog():
    amqp_setup.check_setup()

    queue_name = 'Error'

    # set up a consumer and start to wait for coming messages
    amqp_setup.channel.basic_consume(
        queue=queue_name, on_message_callback=callback, auto_ack=True)
    # an implicit loop waiting to receive messages;
    amqp_setup.channel.start_consuming()
    # it doesn't exit by default. Use Ctrl+C in the command window to terminate it.


# required signature for the callback; no return
def callback(channel, method, properties, body):
    print("\nReceived an error log")
    # processOrderLog(json.loads(body))

    # comment out first
    # processSMS()
    processemail()
    print("SMSSSSS SENTTTTT")  # print a new line feed

    print("\nReceived an error by " + __file__)
    processError(body)
    print()  # print a new line feed


def processSMS():
    print("Printing the error message:")
    try:

        print("There's an error authorising access")
    except Exception as e:
        print("There's an error authorising access")
    print()

    print("Sending an sms")
    account_sid = "AC94cbf138c93df61491a51bb6d6782d7b"
    auth_token = "0cd5fa293cc5c029a565ce0227d54b65"
    client = Client(account_sid, auth_token)

    message = client.messages.create(
        body="There's an error authorising access",
        from_="+12766336073",
        to="+6581919797"
    )

    print(message.sid)


def processError(errorMsg):
    print("Printing the error message:")
    try:
        error = json.loads(errorMsg)
        print("--JSON:", error)
    except Exception as e:
        print("--NOT JSON:", e)
        print("--DATA:", errorMsg)
    print()


def processemail():
    subject = "Recent allowed access"
    body = "You have receive an error notification."
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
    receiveOrderLog()
