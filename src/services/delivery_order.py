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
class Delivery(db.Model):
    __tablename__ = 'DeliveryOrder'
    delivery_uuid = db.Column(db.String(255), nullable=False, primary_key=True)
    delivery_date = db.Column(db.String(50), nullable=True)
    delivery_time = db.Column(db.String(50), nullable=True)
    delivery_order_url = db.Column(db.String(15000))
    bidding_uuid = db.Column(db.String(255))

    def __init__(self, delivery_uuid, delivery_date, delivery_time, delivery_order_url, bidding_uuid):
        self.delivery_uuid = delivery_uuid
        self.delivery_date = delivery_date
        self.delivery_time = delivery_time
        self.delivery_order_url = delivery_order_url
        self.bidding_uuid = bidding_uuid

    def json(self):
        return {"Delivery_uuid": self.delivery_uuid, "Delivery_date": self.delivery_date, "Delivery_time": self.delivery_time, "Delivery_Order_URL": self.delivery_order_url, "Bidding_uuid": self.bidding_uuid}
    
    # Delivery Order to be created automatically after purchase order have been created
    @app.route("/v1/delivery_order/create_delivery_order", methods=['POST'])
    def create_delivery_order():
        data = request.get_json()
        print(data)

        if(data):
            delivery_order = Delivery(**data)

            try:
                db.session.add(delivery_order)
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
                    "message": "delivery_order.py internal error: " + ex_str
                }), 500
            
            return jsonify(
                {
                    "code": 200, 
                    "data": {
                        "data": {
                            "Delivery_uuid": data["delivery_uuid"],
                            "Delivery_date": data["delivery_date"],
                            "Delivery_time": data["delivery_time"],
                            "Delivery_Order_URL": data["delivery_order_url"],
                            "Bidding_uuid": data["bidding_uuid"]
                        },
                        "message": "Delivery Order for " + data["delivery_uuid"] + " have been created." 
                    }
                }
            ),201
        else:
            return jsonify({
                "code": 400,
                "message": "Invalid JSON input: " + str(request.get_data())
            }), 400

    # Delivery Order to be updated based on the changes to the file contents that will be uploaded.
    @app.route("/v1/delivery_order/update_delivery_order/<string:delivery_uuid>", methods=["PUT"])
    def update_delivery_order(delivery_uuid):
        delivery_order = Delivery.query.filter_by(delivery_uuid=delivery_uuid).first()
        if request.is_json:
            try:
                if delivery_order:
                    data = request.get_json()
                    if data["delivery_order_file_url"]:
                        delivery_order.delivery_order_file_url = data["delivery_order_file_url"]
                    else:
                        delivery_order.delivery_order_file_url = delivery_order.delivery_order_file_url
                    db.session.commit()
                    return jsonify(
                        {
                            "code": 200,
                            "data": {
                                "delivery_order_result": {
                                    "delivery_order_details": delivery_order.json()
                                }
                            }
                        }
                    ), 201
                return jsonify( 
                    {
                        "code": 404, 
                        "data": {
                            "Message": "Unable to locate Delivery Order"
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
                    "message": "delivery_order.py internal error: " + ex_str
                }), 500

        # if reached here, not a JSON request.
        return jsonify({
            "code": 400,
            "message": "Invalid JSON input: " + str(request.get_data())
        }), 400

    # Get a collection of all the delivery orders
    @app.route("/v1/delivery_order/get_all_delivery_orders")
    def get_list_of_delivery_orders():
        delivery_order_lists = Delivery.query.all()
        try:
            if len(delivery_order_lists):
                return jsonify(
                    {
                        "code": 200,
                        "data": {
                            "Published_Deliverys": [delivery_orders_published.json() for delivery_orders_published in delivery_order_lists]
                        }
                    }
                )
            else:
                return jsonify(
                    {
                        "code": 404,
                        "message": "There are no delivery_orders created."
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
                "message": "delivery_order.py internal error: " + ex_str
            }), 500

    # Retrieve specific delivery orders by ID
    @app.route("/v1/delivery_order/get_delivery_order_by_id/<string:delivery_uuid>")
    def find_delivery_order_published_by_id(delivery_uuid):
        delivery_order = Delivery.query.filter_by(delivery_uuid=delivery_uuid).first()
        try:
            if delivery_order:
                return jsonify(
                    {
                        "code": 200,
                        "data": {
                            "delivery_order": delivery_order.json()
                        }
                }
            )
            else:
                return jsonify(
                    {
                        "code": 404,
                        "message": "Delivery_Order not found"
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


# Table for Delivery_Order 
class Purchase_Delivery(db.Model):
    __tablename__ = 'Purchase_Delivery'
    Purchase_Delivery_uuid = db.Column(db.String(255), nullable=False, primary_key=True)
    PurchaseUID = db.Column(db.String(255), nullable=False)
    DeliveryUID = db.Column(db.String(255), nullable=False)

    def __init__(self, Purchase_Delivery_uuid, PurchaseUID, DeliveryUID):
        self.Purchase_Delivery_uuid = Purchase_Delivery_uuid
        self.PurchaseUID = PurchaseUID
        self.DeliveryUID = DeliveryUID

    def json(self):
        return {"Purchase_Delivery_uuid": self.Purchase_Delivery_uuid, "PurchaseUID": self.PurchaseUID, "DeliveryUID": self.DeliveryUID}
    
    # Purchase_Delivery_Order will be created automatically once delivery_order is created for the purchase order for tracking purposes.
    @app.route("/v1/purchase_delivery/create_purchase_delivery_order", methods=['POST'])
    def create_purchase_delivery_order():
        data = request.get_json()
        
        purchase_delivery = Purchase_Delivery(**data)

        try:
            db.session.add(purchase_delivery)
            db.session.commit()

            return jsonify(
            {
                "code": 200, 
                "data": {
                    "Purchase_Delivery_UUID": data["Purchase_Delivery_uuid"],
                    "PurchaseUID": data["PurchaseUID"],
                    "DeliveryUID": data["DeliveryUID"],
                },
                "message": "Purchase Delivery Order " + data["Purchase_Delivery_uuid"] + " have been created."
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
                "message": "bidding.py internal error: " + ex_str
            }), 500

    # Getting a collection of all the purchase_delivery_orders for tracking purposes.
    @app.route("/v1/purchase_delivery/get_all_purchase_delivery_orders")
    def get_list_of_purchase_delivery_orders():
        purchase_delivery_order_lists = Purchase_Delivery.query.all()
        try:
            if len(purchase_delivery_order_lists):
                return jsonify(
                    {
                        "code": 200,
                        "data": {
                            "Published_Purchase_Delivery_Order": [purchase_delivery_orders_published.json() for purchase_delivery_orders_published in purchase_delivery_order_lists]
                        }
                    }
                )
            else:
                return jsonify(
                    {
                        "code": 404,
                        "message": "There are no purchase_delivery_orders created."
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
                "message": "delivery_order.py internal error: " + ex_str
            }), 500

    # Get a purchase_delivery_order by id
    @app.route("/v1/purchase_delivery/get_purchase_delivery_order_by_id/<string:Purchase_Delivery_uuid>")
    def find_purchase_delivery_order_published_by_id(Purchase_Delivery_uuid):
        purchase_delivery_order = Purchase_Delivery.query.filter_by(Purchase_Delivery_uuid=Purchase_Delivery_uuid).first()
        try:
            if purchase_delivery_order:
                return jsonify(
                    {
                        "code": 200,
                        "data": {
                            "purchase_delivery_order": purchase_delivery_order.json()
                        }
                }
            )
            else:
                return jsonify(
                    {
                        "code": 404,
                        "message": "Purchase_Delivery_Order not found"
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
