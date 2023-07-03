from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from datetime import datetime
import json 
import uuid

import os
import sys
from os import environ

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = environ.get("dbURL")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLACHEMY_ENGINE_OPTIONS'] = {'pool_recycle': 299}

db = SQLAlchemy(app)

CORS(app)

# Table for Bidding Event
class Bidding(db.Model):
    __tablename__ = 'bidding'
    bidding_uuid = db.Column(db.String(255), nullable=False, primary_key=True)
    title = db.Column(db.String(100), nullable=True)
    description = db.Column(db.String(500), nullable=True)
    bidding_date = db.Column(db.String(50), nullable=True)
    bidding_time = db.Column(db.String(50), nullable=True)
    num_of_vehicles = db.Column(db.Integer)

    def __init__(self, bidding_uuid, title, description, bidding_date, bidding_time, num_of_vehicles):
        self.bidding_uuid = bidding_uuid
        self.title = title
        self.description = description
        self.bidding_date = bidding_date
        self.bidding_time = bidding_time # Time of bidding period ends
        self.num_of_vehicles = num_of_vehicles

    def json(self):
        return {"Bidding_uuid": self.bidding_uuid, "Title": self.title, "Description": self.description, "Bidding_Date": self.bidding_date, "Bidding_Time": self.bidding_time, "Num_Of_Vehicles": self.num_of_vehicles}


# Relational Table for Bidding and User
# Table for Bidding Event
class Bidding_Offer(db.Model):
    __tablename__ = 'Bidding_Offer'
    bidding_offer_uuid = db.Column(db.String(255), nullable=False, primary_key=True)
    bid_price = db.Column(db.String(255), nullable=True)
    UserUID = db.Column(db.String(255), nullable=True)
    BiddingUID = db.Column(db.String(255), nullable=True)
    Bidding_Offer_Result = db.Column(db.String(45), nullable=True)

    def __init__(self, bidding_offer_uuid, bid_price, UserUID, BiddingUID, Bidding_Offer_Result):
        self.bidding_offer_uuid = bidding_offer_uuid
        self.bid_price = bid_price
        self.UserUID = UserUID
        self.BiddingUID = BiddingUID
        self.Bidding_Offer_Result = Bidding_Offer_Result

    def json(self):
        return {"Bidding_Offer_uuid": self.bidding_offer_uuid, "Bid_Price": self.bid_price, "UserUID": self.UserUID, "BiddingUID": self.BiddingUID, "Bidding_Offer_Result": self.Bidding_Offer_Result}
    
    # A bidding offer will be created after the delivery partner has submitted their offer.
    # An email will be sent to the delivery provider after an offer is submitted. 
    @app.route("/v1/bidding_offer/create_bidding_offer/<string:UserUID>/<string:bidding_uuid>", methods=['POST'])
    def create_bidding_offer(UserUID, bidding_uuid):
        data = request.get_json()

        bid_offer = Bidding.query.filter_by(bidding_uuid=bidding_uuid).first()
        exist_bid = Bidding_Offer.query.filter_by(UserUID=UserUID, BiddingUID=bidding_uuid).first()
    
        if bid_offer:
            if not exist_bid:
                bidding_offer = Bidding_Offer(**data)
                try:
                    db.session.add(bidding_offer)
                    db.session.commit()
                except Exception as e:
                    # Unexpected error in code
                    exc_type, exc_obj, exc_tb = sys.exc_info()
                    fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
                    ex_str = str(e) + " at " + str(exc_type) + ": " + \
                        fname + ": line " + str(exc_tb.tb_lineno)
                    print(ex_str)

                    return jsonify({
                        "code": 500,
                        "message": "bidding.py internal error: " + ex_str
                    }), 500
                
                return jsonify(
                    {
                        "code": 200, 
                        "data": {
                            "Bidding_Offer_UUID": data["bidding_offer_uuid"],
                            "Bid_Price": data["bid_price"],
                            "UserUID": data["UserUID"],
                            "BiddingUID": data["BiddingUID"]
                        },
                        "message": "Bidding Offer of " + data["bid_price"] + " have been confirmed. Results of the bid will be notified after the bidding has ended." 
                    },200
                )
            else:
                return jsonify(
                {
                    "code": 400, 
                    "data": {
                        "Bidding_Offer_UUID": data["bidding_offer_uuid"],
                        "Bid_Price": data["bid_price"],
                        "UserUID": data["UserUID"],
                        "BiddingUID": data["BiddingUID"]
                    },
                    "message": "Bidding Offer already exists."  
                }
            ),400
        else:
            return jsonify({
                    "code": 500,
                    "message": "bidding.py internal error: " + ex_str
                }), 500

    # Display all the bidding offers that the bidding have received from the delivery partners
    ## Note: Display all bidding offers in incremental order at frontend js
    @app.route("/v1/bidding_offer/get_all_bidding_offers/<string:BiddingUID>")
    def get_list_of_bidding_offers(BiddingUID):
        bidding_offer_lists = Bidding_Offer.query.filter_by(BiddingUID=BiddingUID).all()
        try:
            if len(bidding_offer_lists):
                return jsonify(
                    {
                        "code": 200,
                        "data": {
                            "Published_Biddings": [biddings_offer_published.json() for biddings_offer_published in bidding_offer_lists]
                        }
                    }
                )
            else:
                return jsonify(
                    {
                        "code": 404,
                        "message": "There are no bidding offer."
                    }
                ), 404
        except Exception as e:
            # Unexpected error in code
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            ex_str = str(e) + " at " + str(exc_type) + ": " + \
                fname + ": line " + str(exc_tb.tb_lineno)
            print(ex_str)

            return jsonify({
                "code": 500,
                "message": "bidding.py internal error: " + ex_str
            }), 500

    # Get a specific bidding offer from a delivery partner to retrieve more details (e.g., Reviews/Ratings/Security Documents - KIV)
    @app.route("/v1/bidding_offer/get_bidding_offer_by_id/<string:bidding_offer_uuid>")
    def find_bidding_offer_by_id(bidding_offer_uuid):
        bidding_offer = Bidding_Offer.query.filter_by(bidding_offer_uuid=bidding_offer_uuid).first()
        try:
            if bidding_offer:
                return jsonify(
                    {
                        "code": 200,
                        "data": {
                            "bidding": bidding_offer.json()
                        }
                }
            )
            else:
                return jsonify(
                    {
                        "code": 404,
                        "message": "Bidding Offer not found"
                    }
                ),404
        except Exception as e:
            # Unexpected error in code
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            ex_str = str(e) + " at " + str(exc_type) + ": " + \
                fname + ": line " + str(exc_tb.tb_lineno)
            print(ex_str)

            return jsonify({
                "code": 500,
                "message": "bidding.py internal error: " + ex_str
            }), 500

    # The acceptance or rejection of the bids will be performed automatically by the web portal after the bidding date/time have past.
    # The web portal will be programmed to accept the lowest bid that a delivery partner have offered.
    # A email notification will be triggered to all parties on the result of their bids.
    @app.route("/v1/bidding_offer/update_bidding_offer/<string:bidding_offer_uuid>", methods=["PUT"])
    def update_bidding_offer(bidding_offer_uuid):
        bidding_offer = Bidding_Offer.query.filter_by(bidding_offer_uuid=bidding_offer_uuid).first()
        if request.is_json:
            try:
                if bidding_offer:
                    data = request.get_json()
                    if data["bid_price"]:
                        bidding_offer.bid_price = data["bid_price"]
                    else:
                        bidding_offer.bid_price = bidding_offer.bid_price
                    db.session.commit()
                    return jsonify(
                        {
                            "code": 200,
                            "data": {
                                "bidding_result": {
                                    "bidding_details": bidding_offer.json()
                                }
                            }
                        }
                    ), 201
                return jsonify( 
                    {
                        "code": 404, 
                        "data": {
                            "Bidding_UUID": bidding_offer.bidding_offer_uuid,
                            "Message": "Bidding Offer not found."
                        }
                    }
                ), 404
            except Exception as e:
                # Unexpected error in code
                exc_type, exc_obj, exc_tb = sys.exc_info()
                fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
                ex_str = str(e) + " at " + str(exc_type) + ": " + \
                    fname + ": line " + str(exc_tb.tb_lineno)
                print(ex_str)

                return jsonify({
                    "code": 500,
                    "message": "bidding.py internal error: " + ex_str
                }), 500

        # if reached here, not a JSON request.
        return jsonify({
            "code": 400,
            "message": "Invalid JSON input: " + str(request.get_data())
        }), 400

# Run this API call to change the status of the bids after the bidding period have ended.
# Check through each bid and pick up the cheapest bid. 
# Once found, accept it and reject the rest. 
# Acceptance of the 1st bid based on lowest costs and Rejection of all other bids to be confirmed later. 
@app.route("/v1/bidding_offer/update_bidding_offer_status/<string:BiddingUID>", methods=["PUT"])
def update_bidding_offer_status(BiddingUID):
    # Retrieve all the bids that are related to the Bidding ID
    bidding_offer = Bidding_Offer.query.filter_by(BiddingUID=BiddingUID).all()

    # return jsonify(
    #     {
    #         "code": 200,
    #         "data": {
    #             "Published_Bids": [bidding_offer_details.json() for bidding_offer_details in bidding_offer]
    #         }      
    #     }
    # ), 201

    # published_bids = []
    # published_bids.append(bidding_offer)

    bid_dict = { "bidding_offer_id": [] , "bidding_offer_price": []}

    if bidding_offer:
        for offer_uid in bidding_offer:
            bid_dict["bidding_offer_id"].append(offer_uid.bidding_offer_uuid)    
        
        for offer_price in bidding_offer:
            bid_dict["bidding_offer_price"].append(offer_price.bid_price)

        min_price = bid_dict["bidding_offer_price"][0]
        for price in bid_dict["bidding_offer_price"]:
            if price < min_price:
                min_price = price

        for bids in bid_dict["bidding_offer_price"]:
            if min_price == bids:
                selected_index =  bid_dict["bidding_offer_price"].index(min_price)
                selected_bid_offer_uuid = bid_dict["bidding_offer_id"][selected_index]
                break

        # Determine the lowest bid offer and auto accepting the bid
        selected_bid_offer = Bidding_Offer.query.filter_by(bidding_offer_uuid = selected_bid_offer_uuid).first()

        if request.is_json:
            try:
                if selected_bid_offer:
                    data = request.get_json()
                    if data["Bidding_Offer_Result"]:
                        selected_bid_offer.Bidding_Offer_Result = data["Bidding_Offer_Result"]
                    else:
                        selected_bid_offer.Bidding_Offer_Result = selected_bid_offer.Bidding_Offer_Result
                    db.session.commit()
                    return jsonify(
                        {
                            "code": 200,
                            "data": {
                                "bidding_result": {
                                    "bidding_details": selected_bid_offer.json()
                                }
                            }
                        }
                    ), 201
                return jsonify( 
                    {
                        "code": 404, 
                        "data": {
                            "Bidding_UUID": selected_bid_offer.bidding_offer_uuid,
                            "Message": "Bidding Offer not found."
                        }
                    }
                ), 404
            except Exception as e:
                # Unexpected error in code
                exc_type, exc_obj, exc_tb = sys.exc_info()
                fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
                ex_str = str(e) + " at " + str(exc_type) + ": " + \
                    fname + ": line " + str(exc_tb.tb_lineno)
                print(ex_str)

                return jsonify({
                    "code": 500,
                    "message": "bidding.py internal error: " + ex_str
                }), 500

        # if reached here, not a JSON request.
        return jsonify({
            "code": 400,
            "message": "Invalid JSON input: " + str(request.get_data())
        }), 400

## Continue from previous API call for rejection of bids
# Run this API call to change the status of the bids after the bidding period have ended.
# Check through each bid and pick up the cheapest bid. 
# Once found, accept it and reject the rest. 
# Acceptance of the 1st bid based on lowest costs and Rejection of all other bids to be confirmed later. 
@app.route("/v1/bidding_offer/update_bidding_offer_status_rejection/<string:BiddingUID>", methods=["PUT"])
def update_bidding_offer_status_rejected(BiddingUID):
    # Retrieve all the bids that are related to the Bidding ID
    bidding_offer = Bidding_Offer.query.filter_by(BiddingUID=BiddingUID).all()

    bid_dict = { "bidding_offer_id": [] , "bidding_offer_price": []}

    if bidding_offer:
        for offer_uid in bidding_offer:
            bid_dict["bidding_offer_id"].append(offer_uid.bidding_offer_uuid)    
        
        for offer_price in bidding_offer:
            bid_dict["bidding_offer_price"].append(offer_price.bid_price)

        min_price = bid_dict["bidding_offer_price"][0]
        for price in bid_dict["bidding_offer_price"]:
            if price < min_price:
                min_price = price

        for bids in bid_dict["bidding_offer_price"]:
            if min_price == bids:
                selected_index =  bid_dict["bidding_offer_price"].index(min_price)
                bid_dict["bidding_offer_price"].remove(min_price)
                selected_bid_offer_uuid = bid_dict["bidding_offer_id"][selected_index]
                bid_dict["bidding_offer_id"].remove(selected_bid_offer_uuid)
                break

        for remain_bids in bid_dict["bidding_offer_id"]:
            # Loop through all the remaining bids and updated as rejected
            rejected_bid_offer = Bidding_Offer.query.filter_by(bidding_offer_uuid = remain_bids).first()

            if request.is_json:
                try:
                    if rejected_bid_offer:
                        data = request.get_json()
                        if data["Bidding_Offer_Result"]:
                            rejected_bid_offer.Bidding_Offer_Result = data["Bidding_Offer_Result"]
                        else:
                            rejected_bid_offer.Bidding_Offer_Result = rejected_bid_offer.Bidding_Offer_Result
                        db.session.commit()
                except Exception as e:
                    # Unexpected error in code
                    exc_type, exc_obj, exc_tb = sys.exc_info()
                    fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
                    ex_str = str(e) + " at " + str(exc_type) + ": " + \
                        fname + ": line " + str(exc_tb.tb_lineno)
                    print(ex_str)

                    return jsonify({
                        "code": 500,
                        "message": "bidding.py internal error: " + ex_str
                    }), 500

            # if reached here, not a JSON request.
            # return jsonify({
            #     "code": 400,
            #     "message": "Invalid JSON input: " + str(request.get_data())
            # }), 400
        return jsonify(
            {
                "code": 200,
                "data": {
                    "bidding_result": {
                        "bidding_details": rejected_bid_offer.json()
                    }
                }
            }
        ), 201
    return jsonify( 
        {
            "code": 404, 
            "data": {
                "Bidding_UUID": rejected_bid_offer.bidding_offer_uuid,
                "Message": "Bidding Offer not found."
            }
        }
    ), 404

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5001, debug=True)