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
    @app.route("/v1/purchase_delivery/create_purchase_delivery_order/<string:PurchaseUID>/<string:DeliveryUID>", methods=['POST'])
    def create_purchase_delivery_order(PurchaseUID, DeliveryUID):
        data = request.get_json()

        purchase_delivery_details = Purchase_Delivery.query.filter_by(PurchaseUID=PurchaseUID, DeliveryUID=DeliveryUID).first()

        try:
            if not purchase_delivery_details:
                PD_UID = str(uuid.uuid4())
                purchase_delivery = Purchase_Delivery(PD_UID, PurchaseUID, DeliveryUID)

                db.session.add(purchase_delivery)
                db.session.commit()

                return jsonify(
                {
                    "code": 200, 
                    "data": {
                        "Purchase_Delivery_UUID": PD_UID,
                        "PurchaseUID": PurchaseUID,
                        "DeliveryUID": DeliveryUID,
                    },
                    "message": "Purchase Delivery Order " + PD_UID + " have been created."
                }
            ),201
            else:
                return jsonify(
                {
                    "code": 400, 
                    "data": {
                        "PurchaseUID": PurchaseUID,
                        "DeliveryUID": DeliveryUID,
                    },
                    "message": "Purchase Delivery Order with Purchase UID: " + PurchaseUID + " and Delivery UID: " + DeliveryUID + " have already been created."
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