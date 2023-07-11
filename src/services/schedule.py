## This file is implemented for simulation purposes. 
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

# Table for Schedule 
class Schedule(db.Model):
    __tablename__ = 'Schedule'
    purchase_uid = db.Column(db.String(255), nullable=False, primary_key=True)
    delivery_uid = db.Column(db.String(255), nullable=False, primary_key=True)
    schedule_summary = db.Column(db.String(255), nullable=False)
    schedule_description = db.Column(db.String(255), nullable=False)
    schedule_start_date = db.Column(db.String(50), nullable=False)
    schedule_start_time = db.Column(db.String(50), nullable=False)
    schedule_end_date = db.Column(db.String(50), nullable=False)
    schedule_end_time = db.Column(db.String(50), nullable=False)
    schedule_from_location = db.Column(db.String(255), nullable=False)
    schedule_to_location = db.Column(db.String(255), nullable=False)
    priority_level = db.Column(db.String(50), nullable=False)
    calendar_uuid = db.Column(db.String(255), nullable=False)

    def __init__(self, purchase_uid, delivery_uid, schedule_summary, schedule_description, schedule_start_date, schedule_start_time, schedule_end_date, schedule_end_time, schedule_from_location, schedule_to_location, priority_level, calendar_uuid):
        self.purchase_uid = purchase_uid
        self.delivery_uid = delivery_uid
        self.schedule_summary = schedule_summary
        self.schedule_description = schedule_description
        self.schedule_start_date = schedule_start_date
        self.schedule_start_time = schedule_start_time
        self.schedule_end_date = schedule_end_date
        self.schedule_end_time = schedule_end_time
        self.schedule_from_location = schedule_from_location
        self.schedule_to_location = schedule_to_location
        self.priority_level = priority_level
        self.calendar_uuid = calendar_uuid


    def json(self):
        return {"purchase_uid": self.purchase_uid, "delivery_uid": self.delivery_uid, "schedule_summary": self.schedule_summary, "schedule_description": self. schedule_description, 
                "schedule_start_date": self.schedule_start_date, "schedule_start_time": self.schedule_start_time, "schedule_end_date": self.schedule_end_date, "schedule_end_time": self.schedule_end_time,
                "schedule_from_location": self.schedule_from_location, "schedule_to_location": self.schedule_to_location, "priority_level": self.priority_level, "calendar_uuid": self.calendar_uuid}
    
    # 1. In Complex MS, retrieve the details from Delivery_Order MS, trigger create_schedule function, then update delivery order with the scheduled date and time for delivery
    # 2. Delivery Order will be updated with the delivery date and time once scheduling have been trigger with the relevant information generated.
    # 3. After the delivery order has been updated with the date and time, create an event in the google calendar synchronously and display on the calendar UI
    @app.route("/v1/schedule/create_schedule/<string:purchase_uid>/<string:delivery_uid>", methods=['POST'])
    def create_schedule(purchase_uid, delivery_uid):
        data = request.get_json()

        scheduling_details = Schedule.query.filter_by(purchase_uid=purchase_uid, delivery_uid=delivery_uid).first()

        try:
            if not scheduling_details:
                schedule_details = Schedule(**data)

                db.session.add(schedule_details)
                db.session.commit()

                return jsonify(
                {
                    "code": 200, 
                    "data": {
                        "PurchaseUID": purchase_uid,
                        "DeliveryUID": delivery_uid,
                    },
                    "message": "Delivery Date and Time for Delivery Order " + delivery_uid + " or for Purchase Order " + purchase_uid + " have been created."
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

    # Getting a collection of all the scheduled orders for tracking purposes.
    @app.route("/v1/schedule/get_all_schedule")
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

    # Get a schedule by id
    @app.route("/v1/schedule/get_schedule_by_id/<string:purchase_uid>/<string:delivery_uid>")
    def find_schedule_by_id(purchase_uid, delivery_uid):
        schedule = Schedule.query.filter_by(purchase_uid=purchase_uid, delivery_uid=delivery_uid).first()
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
                        "message": "Scheduling for Delivery Order ID: " + delivery_uid + " or Purchase Order ID: " + purchase_uid + " not found."
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
    app.run(host='0.0.0.0', port=5003, debug=True)
