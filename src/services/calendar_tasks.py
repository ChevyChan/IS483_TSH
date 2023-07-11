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

# Table for Calendar Tasks
class Calendar_Tasks(db.Model):
    __tablename__ = 'Tasks'
    task_uuid = db.Column(db.String(255), nullable=False, primary_key=True)
    task_name = db.Column(db.String(100), nullable=False)
    task_date = db.Column(db.String(45), nullable=False) 
    task_time = db.Column(db.String(45), nullable=False)
    task_description = db.Column(db.String(300), nullable=False)
    priority_level = db.Column(db.String(50), nullable = False)
    task_completed = db.Column(db.String(45), nullable=False)
    user_uid = db.Column(db.String(255), nullable=False)
    calendar_uid = db.Column(db.String(255), nullable=False)


    def __init__(self, task_uuid, task_name, task_date, task_time, task_description, priority_level, task_completed, user_uid, calendar_uid):
        self.task_uuid = task_uuid
        self.task_name = task_name
        self.task_date = task_date
        self.task_time = task_time
        self.task_description = task_description
        self.priority_level = priority_level
        self.task_completed = task_completed
        self.user_uid = user_uid
        self.calendar_uid = calendar_uid

    def json(self):
        return {"task_uuid": self.task_uuid, "task_name": self.task_name, "task_date": self.task_date, "task_time": self.task_time, "task_description": self.task_description,
                "priority_level": self.priority_level, "task_completed": self.task_completed, "user_uid": self.user_uid, "calendar_uid": self.calendar_uid}
    
    @app.route("/v1/calendar_tasks/create_calendar_task", methods=['POST'])
    def create_task():
        data = request.get_json()

        try:
            Task_UID = str(uuid.uuid4())
            task_details = Calendar_Tasks(Task_UID, **data)

            db.session.add(task_details)
            db.session.commit()

            return jsonify(
            {
                "code": 200, 
                "data": {
                    "Task_UUID": Task_UID,
                },
                "message": "Task " + Task_UID + " have been created."
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
                "message": "calendar_tasks.py internal error: " + ex_str
            }), 500

    # Getting a collection of all the calendar tasks for tracking purposes.
    @app.route("/v1/calendar_tasks/get_all_calendar_tasks")
    def get_list_of_calendars_tasks():
        calendar_tasks_lists = Calendar_Tasks.query.all()
        try:
            if len(calendar_tasks_lists):
                return jsonify(
                    {
                        "code": 200,
                        "data": {
                            "Calendar_Tasks_Details": [task_details.json() for task_details in calendar_tasks_lists]
                        }
                    }
                )
            else:
                return jsonify(
                    {
                        "code": 404,
                        "message": "There are no existing Calendar Tasks."
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
                "message": "calendar_tasks.py internal error: " + ex_str
            }), 500

    # Get a purchase_delivery_order by id
    @app.route("/v1/calendar_tasks/get_calendar_tasks_by_id/<string:task_uuid>")
    def find_calendar_tasks_by_id(task_uuid):
        task_details = Calendar_Tasks.query.filter_by(task_uuid=task_uuid).first()
        try:
            if task_details:
                return jsonify(
                    {
                        "code": 200,
                        "data": {
                            "Task Details": task_details.json()
                        }
                }
            )
            else:
                return jsonify(
                    {
                        "code": 404,
                        "message": "Task Details not found"
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
                "message": "calendar_tasks.py internal error: " + ex_str
            }), 500

    @app.route("/v1/calendar_tasks/update_calendar_tasks/<string:task_uuid>", methods=["PUT"])
    def update_calendar_task(task_uuid):
        task_details = Calendar_Tasks.query.filter_by(task_uuid=task_uuid).first()
        if request.is_json:
            try:
                if task_details:
                    data = request.get_json()
                    if data["task_completed"]:
                        task_details.task_completed = data["task_completed"]
                    else:
                        task_details.task_completed = task_details.task_completed
                    db.session.commit()
                    return jsonify(
                        {
                            "code": 200,
                            "data": {
                                "task_result": {
                                    "task_details": task_details.json()
                                }
                            }
                        }
                    ), 201
                return jsonify( 
                    {
                        "code": 404, 
                        "data": {
                            "Message": "Unable to locate task from Calendar"
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
                    "message": "calendar_tasks.py internal error: " + ex_str
                }), 500

        # if reached here, not a JSON request.
        return jsonify({
            "code": 400,
            "message": "Invalid JSON input: " + str(request.get_data())
        }), 400

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5001, debug=True)
