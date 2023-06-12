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
    
    # Create a bidding for delivery vehicles automatically based on the historical data during the beginning of the month.
    @app.route("/v1/bidding/create_bidding", methods=['POST'])
    def create_bidding():
        data = request.get_json()
        
        bidding_details = Bidding.query.filter_by(bidding_date=data["bidding_date"], bidding_time=data["bidding_time"]).first()

        if not bidding_details :
            try:
                bidding = Bidding(**data)
                db.session.add(bidding)
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
                            "Title": data["title"],
                            "Description": data["description"],
                            "Bidding_Date": data["bidding_date"],
                            "Bidding_Time": data["bidding_time"],
                            "Number_Of_Vehicles": data["num_of_vehicles"]
                        },
                        "message": "Bidding for " + data["title"] + " to reserve " + str(data["num_of_vehicles"]) + " delivery vehicles set to end on " + data["bidding_date"] + " at " + data["bidding_time"] + " have been posted." 
                }
            ),201
        else:
            return jsonify({
                    "code": 400,
                    "message": "Bidding have already been listed"
                }), 400
        
        

    # Update the bidding based on the date/time/number of delivery vehicles required.
    # Every update, trigger an email notification notifying the delivery provider.
    @app.route("/v1/bidding/update_bidding/<string:bidding_uuid>", methods=["PUT"])
    def update_bidding(bidding_uuid):
        bidding = Bidding.query.filter_by(bidding_uuid=bidding_uuid).first()
        if request.is_json:
            try:
                if bidding:
                    data = request.get_json()
                    if data["bidding_date"]:
                        bidding.bidding_date = data["bidding_date"]
                    else:
                        bidding.bidding_date = bidding.bidding_date
                    if data["bidding_time"]:
                        bidding.bidding_time = data["bidding_time"]
                    else:
                        bidding.bidding_time = bidding.bidding_time
                    if data["num_of_vehicles"]:
                        bidding.num_of_vehicles = data["num_of_vehicles"]
                    else:
                        bidding.num_of_vehicles = bidding.num_of_vehicles
                    db.session.commit()
                    return jsonify(
                        {
                            "code": 200,
                            "data": {
                                "bidding_result": {
                                    "bidding_details": bidding.json()
                                }
                            }
                        }
                    ), 201
                return jsonify( 
                    {
                        "code": 404, 
                        "data": {
                            "Bidding_UUID": bidding_uuid
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

    # Get the collection of all the biddings that was listed by the web portal
    @app.route("/v1/bidding/get_all_biddings")
    def get_list_of_biddings_published():
        bidding_lists = Bidding.query.all()
        try:
            if len(bidding_lists):
                return jsonify(
                    {
                        "code": 200,
                        "data": {
                            "Published_Biddings": [biddings_published.json() for biddings_published in bidding_lists]
                        }
                    }
                )
            else:
                return jsonify(
                    {
                        "code": 404,
                        "message": "There are no bids published."
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

    # Get a specific bidding that was listed.
    @app.route("/v1/bidding/get_bidding_published_by_id/<string:bidding_uuid>")
    def find_bidding_published_by_id(bidding_uuid):
        bidding = Bidding.query.filter_by(bidding_uuid=bidding_uuid).first()
        try:
            if bidding:
                return jsonify(
                    {
                        "code": 200,
                        "data": {
                            "bidding": bidding.json()
                        }
                }
            )
            else:
                return jsonify(
                    {
                        "code": 404,
                        "message": "Bidding not found"
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

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5001, debug=True)
