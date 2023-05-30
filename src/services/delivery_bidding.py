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
    delivery_date = db.Column(db.String(50), nullable=True)
    delivery_time = db.Column(db.String(50), nullable=True)
    bidding_time = db.Column(db.String(50), nullable=True)
    delivery_address = db.Column(db.String(100))
    poc_name = db.Column(db.String(50))
    poc_email = db.Column(db.String(50))
    poc_contact = db.Column(db.String(100))
    purchase_order_url = db.Column(db.String(15000))

    def __init__(self, bidding_uuid, title, description, delivery_date, delivery_time, bidding_time, delivery_address, poc_name, poc_email, poc_contact, purchase_order_url):
        self.bidding_uuid = bidding_uuid
        self.title = title
        self.description = description
        self.delivery_date = delivery_date
        self.delivery_time = delivery_time
        self.bidding_time = bidding_time # Time of bidding period ends
        self.delivery_address = delivery_address
        self.poc_name = poc_name
        self.poc_email = poc_email
        self.poc_contact = poc_contact
        self.purchase_order_url = purchase_order_url

    def json(self):
        return {"Bidding_uuid": self.bidding_uuid, "Title": self.title, "Description": self.description, "Delivery_Date": self.delivery_date, "Delivery_Time": self.bidding_time, "Bidding_Time": self.bidding_time, "Delivery_Address": self.delivery_address, "POC_Name": self.poc_name, "POC_Email": self.poc_email, "POC_Contact": self.poc_contact, "Purchase_Order_URL": self.purchase_order_url}
    
    @app.route("/v1/bidding/create_bidding", methods=['POST'])
    def create_bidding():
        data = request.get_json()
        print(data)

        if(Bidding.query.filter_by(title=data["title"], description=data["description"], delivery_date=data["delivery_date"], delivery_time=data["delivery_time"]).first()):
            return jsonify(
                {
                    "code": 400, 
                    "data": {
                        "Title": data["title"],
                        "Description": data["description"],
                        "Delivery_Date": data["delivery_date"],
                        "Delivery_Time": data["delivery_time"]
                    },
                    "message": "Bidding for " + data["title"] + " set to deliver order(s) on " + data["delivery_date"] + " at " + data["delivery_time"] + " have been posted." 
                },400
            )
        
        bidding = Bidding(**data)

        try:
            db.session.add(bidding)
            db.session.commit()
        except:
            return jsonify(
                {
                    "code": 500,
                    "data": {
                        "message": "An error occured while creating the Bidding."
                    }
                },
            ),500
        
        return jsonify(
            {
                "code": 200, 
                "data": {
                    "bidding_result": {
                        "bidding_details": bidding.json()
                    }
                }
            }
        ),201

    @app.route("/v1/bidding/update_bidding/<string:bidding_uuid>", methods=["PUT"])
    def update_bidding(bidding_uuid):
        bidding = Bidding.query.filter_by(bidding_uuid=bidding_uuid).first()
        if request.is_json:
            try:
                if bidding:
                    data = request.get_json()
                    if data["delivery_date"]:
                        bidding.delivery_date = data["delivery_date"]
                    else:
                        bidding.delivery_date = bidding.delivery_date
                    if data["delivery_time"]:
                        bidding.delivery_time = data["delivery_time"]
                    else:
                        bidding.delivery_time = bidding.delivery_time
                    if data["delivery_address"]:
                        bidding.delivery_address = data["delivery_address"]
                    else:
                        bidding.delivery_address = bidding.delivery_address
                    if data["poc_name"]:
                        bidding.poc_name = data["poc_name"]
                    else:
                        bidding.poc_name = bidding.poc_name
                    if data["poc_email"]:
                        bidding.poc_email = data["poc_email"]
                    else:
                        bidding.poc_email = bidding.poc_email
                    if data["poc_contact"]:
                        bidding.poc_contact = data["poc_contact"]
                    else:
                        bidding.poc_contact = bidding.poc_contact
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
                    "message": "events.py internal error: " + ex_str
                }), 500

        # if reached here, not a JSON request.
        return jsonify({
            "code": 400,
            "message": "Invalid JSON input: " + str(request.get_data())
        }), 400

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
                "message": "deliver_bidding.py internal error: " + ex_str
            }), 500

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
                "message": "deliver_bidding.py internal error: " + ex_str
            }), 500

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5001, debug=True)
