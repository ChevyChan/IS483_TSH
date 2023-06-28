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

# Table for Calendar
class Calendar_App(db.Model):
    __tablename__ = 'Calendar'
    calendar_uuid = db.Column(db.String(255), nullable=False, primary_key=True)
    calendar_name = db.Column(db.String(50), nullable=False)
    provider_name = db.Column(db.String(50), nullable=False)
    user_uuid = db.Column(db.String(255), nullable=False)

    def __init__(self, calendar_uuid, calendar_name, provider_name, user_uuid):
        self.calendar_uuid = calendar_uuid
        self.calendar_name = calendar_name
        self.provider_name = provider_name
        self.user_uuid = user_uuid

    def json(self):
        return {"Calendar_UUID": self.calendar_uuid, "Calendar_Name": self.calendar_name, "Provider_Name": self.provider_name, "User_UUID": self.user_uuid}
    
    @app.route("/v1/calendar/create_calendar", methods=['POST'])
    def create_calendar():
        data = request.get_json()

        try:
            Calendar_UID = str(uuid.uuid4())
            calendar_details = Calendar_App(Calendar_UID, **data)

            db.session.add(calendar_details)
            db.session.commit()

            return jsonify(
            {
                "code": 200, 
                "data": {
                    "Calendar_UUID": Calendar_UID,
                },
                "message": "Calendar " + Calendar_UID + " have been created."
            }
        ),201
        except Exception as e:
            # Unexpected error in code
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            ex_str = str(e) + " at " + str(exc_type) + ": " + \
                fname + ": line " + str(exc_tb.tb_lineno)
            print(ex_str)

            return jsonify({
                "code": 500,
                "message": "Calendar.py internal error: " + ex_str
            }), 500

    # Getting a collection of all the calendars.
    @app.route("/v1/calendar/get_all_calendars")
    def get_list_of_calendars():
        calendar_lists = Calendar_App.query.all()
        try:
            if len(calendar_lists):
                return jsonify(
                    {
                        "code": 200,
                        "data": {
                            "Calendar_Details": [calendar_details.json() for calendar_details in calendar_lists]
                        }
                    }
                )
            else:
                return jsonify(
                    {
                        "code": 404,
                        "message": "There are no existing Calendars."
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
                "message": "calendar.py internal error: " + ex_str
            }), 500

    # Get a purchase_delivery_order by id
    @app.route("/v1/calendar/get_calendar_by_id/<string:calendar_uuid>")
    def find_calendar_by_id(calendar_uuid):
        calendar_details = Calendar_App.query.filter_by(calendar_uuid=calendar_uuid).first()
        try:
            if calendar_details:
                return jsonify(
                    {
                        "code": 200,
                        "data": {
                            "Calendar Details": calendar_details.json()
                        }
                }
            )
            else:
                return jsonify(
                    {
                        "code": 404,
                        "message": "Calendar Details not found"
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
                "message": "calendar.py internal error: " + ex_str
            }), 500

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5001, debug=True)
