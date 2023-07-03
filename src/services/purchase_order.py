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

# Table for Purchase_Order
class Purchase(db.Model):
    __tablename__ = 'PurchaseOrder'
    purchase_uuid = db.Column(db.String(255), nullable=False, primary_key=True)
    purchase_date = db.Column(db.String(50), nullable=True)
    purchase_order_file_url = db.Column(db.String(15000))
    UserUID = db.Column(db.String(255))

    def __init__(self, purchase_uuid, purchase_date, purchase_order_file_url, UserUID):
        self.purchase_uuid = purchase_uuid
        self.purchase_date = purchase_date
        self.purchase_order_file_url = purchase_order_file_url
        self.UserUID = UserUID

    def json(self):
        return {"Purchase_uuid": self.purchase_uuid, "Purchase_date": self.purchase_date, "Purchase_Order_File_URL": self.purchase_order_file_url, "UserUID": self.UserUID}
    
    # The purchase order will be created by the user through the web portal or it will be simulated
    ## Put this complex MS
        # Read the purchase order data from the excel/PDF file uploaded to Firebase Storage - Retrieve Purchase Order to get the Purchase Order URL
        # Create a csv file for Delivery Order
        # Trigger create delivery order here using requests
        ## Get the response of the delivery_uid
        # # result = requests.post("http://127.0.0.1:5001/v1/delivery_order/create_delivery_order")
        # Unpack the json result and retrieve the delivery uuid
        # # delivery_order_result = json.loads(result)
        # # delivery_uuid = delivery_order_result["delivery_uuid"]

        # Use the PurchaseUID and DeliveryUID to create Purchase_Delivery Order
        ## Parameters are to be filled up
        ### purchase_delivery_result = requests.post("http://127.0.0.1:5001/v1/purchase_delivery/create_purchase_delivery_order/data["purchase_uuid"]/delivery_uuid")
    @app.route("/v1/purchase_order/create_purchase_order", methods=['POST'])
    def create_purchase_order():
        data = request.get_json()
        
        purchase_order = Purchase(**data)

        try:
            db.session.add(purchase_order)
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
                    "Purchase_uuid": data["purchase_uuid"],
                    "Purchase_date": data["purchase_date"],
                    "Purchase_Order_File_URL": data["purchase_order_file_url"],
                    "UserUID": data["UserUID"]
                    },
                    "message": "Purchase Order for " + str(data["UserUID"]) + " have been created." 
                }
        ),201

    # Update the purchase order based on the content of the purchase order document.
    # After purchase order have been updated, the web portal will trigger an update to the delivery order.
    @app.route("/v1/purchase_order/update_purchase/<string:purchase_uuid>", methods=["PUT"])
    def update_purchase(purchase_uuid):
        purchase_order = Purchase.query.filter_by(purchase_uuid=purchase_uuid).first()
        if request.is_json:
            try:
                if purchase_order:
                    data = request.get_json()
                    if data["purchase_order_file_url"]:
                        purchase_order.purchase_order_file_url = data["purchase_order_file_url"]
                    else:
                        purchase_order.purchase_order_file_url = purchase_order.purchase_order_file_url
                    db.session.commit()
                    return jsonify(
                        {
                            "code": 200,
                            "data": {
                                "purchase_order_result": {
                                    "purchase_order_details": purchase_order.json()
                                }
                            }
                        }
                    ), 201
                return jsonify( 
                    {
                        "code": 404, 
                        "data": {
                            "Message": "Unable to locate Purchase Order"
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
                    "message": "purchase_order.py internal error: " + ex_str
                }), 500

        # if reached here, not a JSON request.
        return jsonify({
            "code": 400,
            "message": "Invalid JSON input: " + str(request.get_data())
        }), 400

    @app.route("/v1/purchase_order/get_all_purchase_orders")
    def get_list_of_purchase_orders():
        purchase_order_lists = Purchase.query.all()
        try:
            if len(purchase_order_lists):
                return jsonify(
                    {
                        "code": 200,
                        "data": {
                            "Published_Purchases": [purchase_orders_published.json() for purchase_orders_published in purchase_order_lists]
                        }
                    }
                )
            else:
                return jsonify(
                    {
                        "code": 404,
                        "message": "There are no purchase_order created."
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
                "message": "purchase_order.py internal error: " + ex_str
            }), 500

    @app.route("/v1/purchase_order/get_purchase_order_by_id/<string:purchase_uuid>")
    def find_purchase_order_published_by_id(purchase_uuid):
        purchase_order = Purchase.query.filter_by(purchase_uuid=purchase_uuid).first()
        try:
            if purchase_order:
                return jsonify(
                    {
                        "code": 200,
                        "data": {
                            "purchase_order": purchase_order.json()
                        }
                }
            )
            else:
                return jsonify(
                    {
                        "code": 404,
                        "message": "Purchase_Order not found"
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
                "message": "purchase_order.py internal error: " + ex_str
            }), 500

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5001, debug=True)
