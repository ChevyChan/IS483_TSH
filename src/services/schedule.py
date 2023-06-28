## This file is implemented for simulation purposes. 
## This is a complex microservice
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

# Table for Delivery_Order 
class Schedule(db.Model):
    __tablename__ = 'Schedule'
    schedule_uuid= db.Column(db.String(255), nullable=False, primary_key=True)
    schedule_date = db.Column(db.String(50), nullable=False)
    schedule_time = db.Column(db.String(50), nullable=False)
    schedule_description = db.Column(db.String(255), nullable=False)
    priority_level = db.Column(db.String(50), nullable=False)
    purchase_uid = db.Column(db.String(255), nullable=False)
    delivery_uid = db.Column(db.String(255), nullable=False)

    def __init__(self, schedule_uuid, schedule_date, schedule_time, schedule_description, priority_level, purchase_uid, delivery_uid):
        self.schedule_uuid = schedule_uuid
        self.schedule_date = schedule_date
        self.schedule_time = schedule_time
        self.schedule_description = schedule_description
        self.priority_level = priority_level
        self.purchase_uid = purchase_uid
        self.delivery_uid = delivery_uid

    def json(self):
        return {"schedule_uuid": self.schedule_uuid, "schedule_date": self.schedule_date, "schedule_time": self.schedule_time, "schedule_description": self.schedule_description, "priority_level": self.priority_level, "purchase_uid": self.purchase_uid, "delivery_uid": self.delivery_uid}
    
    # Purchase_Delivery_Order will be created automatically once delivery_order is created for the purchase order for tracking purposes.
    @app.route("/v1/schedule/create_schedule/<string:purchase_uid>", methods=['POST'])
    def create_schedule(purchase_uid):
        data = request.get_json()

        scheduling_details = Schedule.query.filter_by(purchase_uid=purchase_uid).first()

        try:
            if not scheduling_details:
                Scheduling_UID = str(uuid.uuid4())
                schedule_details = Schedule(Scheduling_UID, **data)

                db.session.add(schedule_details)
                db.session.commit()

                return jsonify(
                {
                    "code": 200, 
                    "data": {
                        "Scheduling_UUID": Scheduling_UID,
                        "PurchaseUID": purchase_uid,
                        "DeliveryUID": delivery_uid,
                    },
                    "message": "Scheduling " + Scheduling_UID + " for Purchase Order " + purchase_uid + " have been created."
                }
            ),201
            else:
                return jsonify(
                {
                    "code": 400, 
                    "data": {
                        "PurchaseUID": purchase_uid,
                        "DeliveryUID": delivery_uid,
                    },
                    "message": "Scheduling for Purchase UID: " + purchase_uid + " and Delivery UID: " + delivery_uid + " have already been created."
                }
            ), 400
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

    # Getting a collection of all the purchase_delivery_orders for tracking purposes.
    @app.route("/v1/schedule/get_all_scheduling")
    def get_list_of_purchase_delivery_orders():
        scheduling_lists = Schedule.query.all()
        try:
            if len(scheduling_lists):
                return jsonify(
                    {
                        "code": 200,
                        "data": {
                            "Scheduling_List": [scheduling_published.json() for scheduling_published in scheduling_lists]
                        }
                    }
                )
            else:
                return jsonify(
                    {
                        "code": 404,
                        "message": "There are no schedules for delivery created."
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
                "message": "schedule.py internal error: " + ex_str
            }), 500

    # Get a purchase_delivery_order by id
    @app.route("/v1/schedule/get_schedule_by_id/<string:schedule_uuid>")
    def find_schedule_by_id(schedule_uuid):
        schedule = Schedule.query.filter_by(schedule_uuid=schedule_uuid).first()
        try:
            if schedule:
                return jsonify(
                    {
                        "code": 200,
                        "data": {
                            "Schedule_Order": schedule.json()
                        }
                }
            )
            else:
                return jsonify(
                    {
                        "code": 404,
                        "message": "Scheduling for ID: " + schedule_uuid + " not found"
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
                "message": "delivery_order.py internal error: " + ex_str
            }), 500

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5001, debug=True)