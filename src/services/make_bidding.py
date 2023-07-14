### Delivery Providers make bids on available Biddable Jobs ###

### Work in Progress ###
from flask import Flask, request, jsonify
from flask_cors import CORS

import os
import sys
from os import environ

import requests
from invokes import invoke_http

# import amqp_setup
import pika
import json

import uuid

app = Flask(__name__)
CORS(app)

retrieve_user_URL = "http://localhost:5008/v1/user/get_user_by_id"
create_bid_URL = "http://localhost:5007/v1/bidding_offer/create_bidding_offer"
accept_bid_URL = "http://localhost:5007/v1/bidding_offer/update_bidding_offer_status"
reject_bid_URL = "http://localhost:5007/v1/bidding_offer/update_bidding_offer_status_rejection"
confirm_bid_URL = "http://localhost:5007/v1/bidding_offer/update_bidding_offer"

# To be executed whenever a delivery provider have made a bid offer
def make_bids(user_uid, bid_uid, bid_price):
    # User makes bid - Create Bidding Offer
    # Invoke the user microservice
    print('\n-----Invoking user microservice-----')

    print("-----Get current user info-----")
    print("**********************************************")

    user_result = invoke_http(retrieve_user_URL + "/" + user_uid, method='GET')
    print('user_result:', user_result)
     
    code = user_result["code"]
    message = json.dumps(user_result)

    if code not in range(200, 300):  # THIS IS FOR USER!!!

        # Inform the error microservice
        # print('\n\n-----Publishing the (user error) message with routing_key=user.error-----')

        # amqp_setup.channel.basic_publish(exchange=amqp_setup.exchangename, routing_key="user.error",
        #                                  body=message, properties=pika.BasicProperties(delivery_mode=2))
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
            "message": "User retrival failure sent for error handling."
        }

    else:
        # 4. Record edit user
        print(
            '\n\n-----Publishing the (User info) message with routing_key=send.notify (TBC)-----')

        # 5. If no error proceed to Bidding Offer!
        # Check the user result; if a failure, send it to the error microservice.

   
        # Invoke the event microservice
        print('\n\n-----Invoking bidding_offer microservice-----')
        UserID = user_result['data']['user_uuid']
        # Enter bidding offer information
        theRequest = {
            "bidding_offer_uuid": str(uuid.uuid4()),
            "bid_price": bid_price,
            "UserUID": UserID,
            "BiddingUID": bid_uid,
            "Bidding_Offer_Result": "Review"
        }
        # bidding_URL = bidding_URL + "/" + UserID + "/" + BiddingID
        print("*************HIIIIII**************")
        print(theRequest)
        bidding_offer_url = create_bid_URL + "/" + UserID + "/" + bid_uid
       # print(theRequest2)
        bidding_offer_result = invoke_http(
            bidding_offer_url, method="POST", json=theRequest)  # used to be json=order_result['data']
        print("bidding_offer_result:", bidding_offer_result, '\n')

        # Check the bidding_offer result;
        # if a failure, send it to the error microservice.
        #message = json.dumps(bidding_offer_result)

        code = bidding_offer_result[0]["code"]
        # @Swinnerton, need to confirm with you on this.
        if code not in range(200, 300, 500):  # THIS IS FOR Bidding Offer!!!
            theRequest2 = {
                "code": 200,
                "data": theRequest
            }

            print(theRequest2)
            
            # Inform the error microservice
            # print('\n\n-----Invoking error microservice as event fails-----')
            print(
                '\n\n-----Publishing the (event error!!!!) message with routing_key=event.error-----')

            # amqp_setup.channel.basic_publish(exchange=amqp_setup.exchangename, routing_key="bidding_offer.error",
            #                                  body=message, properties=pika.BasicProperties(delivery_mode=2))

            print("\nEvent status ({:d}) published to the RabbitMQ Exchange:".format(
                code), bidding_offer_result)

            # 7. Return error
            return {
                "code": 400,
                "data": {
                    "user_result": "",
                    "bidding_offer_result": bidding_offer_result
                },
                "message": "Bidding_Offer error sent for error handling."
            }
        else:
            # 4. Proceed to publish message as user and event have edited successfully
            print(
                '\n\n-----Publishing the (Bidding Offer info) message with routing_key=send.notify-----')
            # event and the user
            # amqp_setup.channel.basic_publish(exchange=amqp_setup.exchangename, routing_key="send.notify",
            #                                  body=message, properties=pika.BasicProperties(delivery_mode=2))

    # After bid has been made, trigger an automated email to the delivery provider
    

    # 7. Return edited user and bidding_offer
    return {
        "code": 201,
        "data": {
            "user_result": user_result,
            "bidding_offer_result": bidding_offer_result
        }
    }
    

# To be executed after the deadline of the Bids have reached
def accept_bidding_offer(bidding_uid):
    # Retrieve all the available bidding offer
    # Accept the lowest bid offer and change status to "Accepted"

    # Invoke the bidding offer microservice
    print('\n\n-----Invoking bidding_offer microservice-----')
    # Update the lowest bid with an "Accepted" status
    theRequest = {
        "Bidding_Offer_Result": "Accepted"
    }
    # bidding_URL = bidding_URL + "/" + UserID + "/" + BiddingID
    print("*************HIIIIII**************")
    print(theRequest)
    bidding_offer_url = accept_bid_URL + "/" + bidding_uid
    # print(theRequest2)
    bidding_offer_result = invoke_http(
        bidding_offer_url, method="PUT", json=theRequest)  # used to be json=order_result['data']
    print("bidding_offer_result:", bidding_offer_result, '\n')
    
    # Send an automated email to the "Accepted" delivery provider to seek confirmation

    return


def confirm_bidding_offer(bidding_offer_uid):
    # Wait for reply by "Selected" delivery provider to "Confirm" job
    
    # Invoking the bidding offer microservice
    print('\n\n-----Invoking bidding_offer microservice => Function: Confirm Bid URL-----')
    # Delivery provider to confirm the offer with an "Confirmed" status
    theRequest = {
        "bid_price": "",
        "Bidding_Offer_Result": "Confirmed"
    }

    bidding_offer_url = confirm_bid_URL + "/" + bidding_offer_uid
    # print(theRequest2)
    bidding_offer_result = invoke_http(
        bidding_offer_url, method="PUT", json=theRequest)  # used to be json=order_result['data']
    print("bidding_offer_result:", bidding_offer_result, '\n')

    # Retrieve the Bidding_UID of the Bidding Offer
    bidding_uid = bidding_offer_result['data']['bidding_result']['bidding_details']['BiddingUID']

    # If confirmed, reject the other bids from other delivery provider
    if(bidding_offer_result["data"]["bidding_result"]["bidding_details"]["Bidding_Offer_Result"] == "Confirmed"):
        # Call reject_bid_url to reject all other bids
        print('\n\n-----Invoking bidding_offer microservice => Function: Reject Bid URL-----')
        theRequest = {
            "bid_price": "",
            "Bidding_Offer_Result": "Rejected"
        }

        bidding_offer_url = reject_bid_URL + "/" + bidding_uid
        bidding_offer_result = invoke_http(
            bidding_offer_url, method="PUT", json=theRequest)
        
        print("bidding_offer_result:", bidding_offer_result, '\n')
    
        return bidding_offer_result
    else:
        print(bidding_offer_result["data"]["bidding_result"]["bidding_details"]["Bidding_Offer_Result"])


def decline_bidding_offer(bidding_offer_uid):
    # Wait for reply by "Selected" delivery provider to "Decline" job
    
    # Invoking the bidding offer microservice
    print('\n\n-----Invoking bidding_offer microservice => Function: Confirm Bid URL-----')
    # Delivery provider to confirm the offer with an "Confirmed" status
    theRequest = {
        "bid_price": "",
        "Bidding_Offer_Result": "Declined"
    }

    bidding_offer_url = confirm_bid_URL + "/" + bidding_offer_uid
    # print(theRequest2)
    bidding_offer_result = invoke_http(
        bidding_offer_url, method="PUT", json=theRequest)  # used to be json=order_result['data']
    print("bidding_offer_result:", bidding_offer_result, '\n')

    # Send an automated email to both TSH and the selected Delivery Provider confirm that they have rejected the job 

    # Get the Bidding_UID from the Bidding Offer
    bidding_uid = bidding_offer_result["data"]["bidding_result"]["bidding_details"]["BiddingUID"]
    print(bidding_uid)

    return accept_bidding_offer(bidding_uid)


# make_bids('5a0138da-13af-4990-be88-1e5781f23925', "3ef26090-8b4c-41af-ab38-5266e8aa728e", "200")
#accept_bidding_offer("3ef26090-8b4c-41af-ab38-5266e8aa728e")
#confirm_bidding_offer("72bc3617-e8bf-49ba-b971-d09fe1739dd6")
#decline_bidding_offer("4d124378-d390-4107-bc58-0e8da73db4bd")