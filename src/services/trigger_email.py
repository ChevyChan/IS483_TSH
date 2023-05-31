from flask import Flask, request, jsonify
from flask_cors import CORS


import os
import sys
from os import environ

import requests
from invokes import invoke_http

import amqp_setup
import pika
import json

app = Flask(__name__)
CORS(app)

# used to be order activity error
# user_URL = environ.get('user_URL') or "http://localhost:8000/userReg"
# bidding_URL = environ.get(
#     'bidding_URL') or "http://localhost:5200/v1/event_registration/approve_student_details"


user_URL = "http://localhost:8000/userReg"
bidding_URL = "http://localhost:5200/v1/event_registration/approve_student_details"


# activity_log_URL = "http://localhost:5003/activity_log"
# error_URL = "http://localhost:5004/error"


@app.route("/trigger_email", methods=['POST'])
def access():
    # Simple check of input format and data of the request are JSON
    if request.is_json:
        try:
            theRequest = request.get_json()  # json include userID, biddingID?
            # to first check if the "bidding" request is json
            print("\nReceived a JSON:", theRequest)

            # do the actual work
            # 1. Send user edit access
            result = processAccess(theRequest)
            print('\n------------------------')
            print('\nresult: ', result)
            return jsonify(result), result["code"]

        except Exception as e:
            # Unexpected error in code
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            ex_str = str(e) + " at " + str(exc_type) + ": " + \
                fname + ": line " + str(exc_tb.tb_lineno)
            print(ex_str)

            return jsonify({
                "code": 500,
                "message": "trigger_email.py internal error: " + ex_str
            }), 500

    # if reached here, not a JSON request.
    return jsonify({
        "code": 400,
        "message": "Invalid JSON input: " + str(request.get_data())
    }), 400


def processAccess(theRequest):
    user_URL = "http://localhost:8000/userReg"
    user_url = "http://localhost:5200/v1/event_registration/approve_student_details"
    # user_URL = environ.get('user_URL') or "http://localhost:8000/userReg"
    # bidding_URL = environ.get(
    #     'bidding_URL') or "http://localhost:5200/v1/event_registration/approve_student_details"

    # 2. Send user edit access
    # Invoke the user microservice
    print('\n-----Invoking user microservice-----')

    theRequest2 = {
        "code": 200,
        "data": theRequest
    }

    print(theRequest2)
    print("**********************************************")

   # user_result = invoke_http(user_URL, method='POST', json=theRequest2)

    # FOR NOW WWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW so will go directly to else
    user_result = ""

    # print('user_result:', user_result)

    # Check the user result; if a failure, send it to the error microservice.

    # code = user_result["code"]
    # FOR NOWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW
    code = 201

    message = json.dumps(user_result)

    if code not in range(200, 300):  # THIS IS FOR USER!!!

        # Inform the error microservice
        print(
            '\n\n-----Publishing the (user error) message with routing_key=user.error-----')

        amqp_setup.channel.basic_publish(exchange=amqp_setup.exchangename, routing_key="user.error",
                                         body=message, properties=pika.BasicProperties(delivery_mode=2))
        # make message persistent within the matching queues until it is received by some receiver
        # (the matching queues have to exist and be durable and bound to the exchange)

        # - reply from the invocation is not used;
        # continue even if this invocation fails
        print("\nUser status ({:d}) published to the RabbitMQ Exchange:".format(
            code), user_result)

        # 7. Return error
        return {
            "code": 500,
            "data": {"user_result": user_result},
            "message": "User edit failure sent for error handling."
        }

    # back up for "event" =-> bidding
    elif False:
        # 4. Record edit user
        print(
            '\n\n-----Publishing the (User info) message with routing_key=send.notify (TBC)-----')

        # no need invoke because invoke user before
        # invoke_http(activity_log_URL, method="POST", json=order_result)

        # send once will do
        # amqp_setup.channel.basic_publish(exchange=amqp_setup.exchangename, routing_key="send.notify",
        #                                  body=message, properties=pika.BasicProperties(delivery_mode=2))

        # print("\nOrder published to RabbitMQ Exchange.\n")
        # - reply from the invocation is not used;
        # continue even if this invocation fails

        # 5. If no error proceed to bidding!
        # Invoke the bidding microservice
        print('\n\n-----Invoking bidding microservice-----')
        # StudentID = theRequest["StudentID"]
        # BiddingID = theRequest["BiddingID"]
        StudentID = "13"
        BiddingID = "14"
        print("*************HIIIIII**************")
        print(theRequest)
        # bidding_URL = "http://localhost:5200/v1/event_registration/approve_student_details"

        # user_URL = environ.get('user_URL') or "http://localhost:8000/userReg"
        # bidding_URL = environ.get(
        #     'bidding_URL') or "http://localhost:5200/v1/event_registration/approve_student_details"

        user_URL = "http://localhost:8000/userReg"
        user_url = "http://localhost:5200/v1/event_registration/approve_student_details"

        user_url = user_url + "/" + StudentID + "/" + BiddingID
       # print(theRequest2)
        user_result = invoke_http(
            user_url, method="POST", json=theRequest)  # used to be json=order_result['data']
        print(user_result)

        # Check the bidding result;
        # if a failure, send it to the error microservice.
        message = json.dumps(user_result)
        code = user_result["code"]
        if code not in range(200, 300, 500):  # THIS IS FOR BIDDING!!!
            theRequest2 = {
                "code": 200,
                "data": theRequest
            }

            print(theRequest2)
            # user_URL = 'http://localhost:8000/userUnreg'
            user_URL = environ.get(
                'user_URL') or "http://localhost:8000/userUnreg"

            user_result = invoke_http(
                user_URL, method='DELETE', json=theRequest2)
            # Inform the error microservice
            # print('\n\n-----Invoking error microservice as bidding fails-----')
            print(
                '\n\n-----Publishing the (bidding error!!!!) message with routing_key=bidding.error-----')

            amqp_setup.channel.basic_publish(exchange=amqp_setup.exchangename, routing_key="bidding.error",
                                             body=message, properties=pika.BasicProperties(delivery_mode=2))

            print("\nBidding status ({:d}) published to the RabbitMQ Exchange:".format(
                code), user_result)

            # 7. Return error
            return {
                "code": 400,
                "data": {
                    "user_result": "",
                    "bidding_result": user_result
                },
                "message": "Bidding error sent for error handling."
            }
        else:
            # 4. Proceed to publish message as user and bidding have edited successfully
            print(
                '\n\n-----Publishing the (Bidding info) message with routing_key=send.notify-----')
            # bidding and the user
            amqp_setup.channel.basic_publish(exchange=amqp_setup.exchangename, routing_key="send.notify",
                                             body=message, properties=pika.BasicProperties(delivery_mode=2))

    else:

        print('\n\n-----Invoking user microservice-----')

        StudentID = "13"
        print("*************HIIIIII**************")
        print(theRequest)

        user_url = "http://localhost:8000/userReg"
       # print(theRequest2)
        user_result = invoke_http(
            user_url, method="POST", json=theRequest)  # used to be json=order_result['data']
        print(user_result)

        # Check the user result;
        # if a failure, send it to the error microservice.
        message = json.dumps(user_result)
        code = user_result["code"]
        if code not in range(200, 300, 500):
            theRequest2 = {
                "code": 200,
                "data": theRequest
            }

            print(theRequest2)
            # user_URL = 'http://localhost:8000/userUnreg'
            user_URL = environ.get(
                'user_URL') or "http://localhost:8000/userUnreg"

            user_result = invoke_http(
                user_URL, method='DELETE', json=theRequest2)
            # Inform the error microservice
            # print('\n\n-----Invoking error microservice as user fails-----')
            print(
                '\n\n-----Publishing the (user error!!!!) message with routing_key=user.error-----')

            amqp_setup.channel.basic_publish(exchange=amqp_setup.exchangename, routing_key="user.error",
                                             body=message, properties=pika.BasicProperties(delivery_mode=2))

            print("HIIII")
            # print("\User status ({:d}) published to the RabbitMQ Exchange:".format(code), user_result)

            # 7. Return error
            return {
                "code": 400,
                "data": {
                    "user_result": user_result,
                    "bidding_result": ""
                },
                "message": "User error sent for error handling."
            }
        else:
            # 4. Proceed to publish message as user have edited successfully
            print(
                '\n\n-----Publishing the (User info) message with routing_key=send.notify-----')
            #  the user
            amqp_setup.channel.basic_publish(exchange=amqp_setup.exchangename, routing_key="send.notify",
                                             body=message, properties=pika.BasicProperties(delivery_mode=2))

    # 7. Return edited user and bidding
    return {
        "code": 201,
        "data": {
            "user_result": user_result,
            "bidding_result": ""
        }
    }


# Execute this program if it is run as a main script (not by 'import')
if __name__ == "__main__":
    print("This is flask " + os.path.basename(__file__) +
          " for editing the access for user and bidding...")
    app.run(host="0.0.0.0", port=5100, debug=True)
    # Notes for the parameters:
    # - debug=True will reload the program automatically if a change is detected;
    #   -- it in fact starts two instances of the same flask program, and uses one of the instances to monitor the program changes;
    # - host="0.0.0.0" allows the flask program to accept requests sent from any IP/host (in addition to localhost),
    #   -- i.e., it gives permissions to hosts with any IP to access the flask program,
    #   -- as long as the hosts can already reach the machine running the flask program along the network;
    #   -- it doesn't mean to use http://0.0.0.0 to access the flask program.
