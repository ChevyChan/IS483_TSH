from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from os import environ

import os
import sys
from os import environ

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('dbURL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {'pool_recycle': 299}

db = SQLAlchemy(app)
CORS(app)


class Company(db.Model):
    __tablename__ = 'Company'

    company_id = db.Column(db.String(255), primary_key=True)
    company_name = db.Column(db.String(255), nullable=False)
    company_address = db.Column(db.String(255), nullable=False)
    company_email = db.Column(db.String(255), nullable=False)
    company_type = db.Column(db.String(30))

    def __init__(self, company_id, company_name, company_address, company_email, company_type):
        self.company_id = company_id
        self.company_name = company_name
        self.company_address = company_address
        self.company_email = company_email
        self.company_type = company_type

    def json(self):
        return {
            "company_id": self.company_id,
            "company_name": self.company_name,
            "company_address": self.company_address,
            "company_email": self.company_email,
            "company_type": self.company_type
        }

@app.route("/v1/company/get_company_by_id/<string:company_id>")
def get_company_by_UUID(company_id):
    company_details = Company.query.filter_by(company_id=company_id).first()
    if company_details:
        return jsonify(
            {
                "code": 200,
                "data": company_details.json()
            }
        )
    return jsonify(
        {
            "code": 404,
            "message": "No user found"
        }
    )

@app.route("/v1/company/create_company", methods=["POST"])
def create_company():
        
    data = request.get_json()
    company = Company(**data)

    try:
        db.session.add(company)
        db.session.commit()
    except:
        return jsonify(
            {
                "code": 500,
                "data": {
                    "company_details": company.json()
                },
                "message": "An error occurred creating company details."
            }
        ), 500

    return jsonify(
        {
            "code": 200,
            "data": company.json()
        }
    ), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)