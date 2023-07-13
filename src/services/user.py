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


class User(db.Model):
    __tablename__ = 'Users'

    user_uuid = db.Column(db.String(255), primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(255), nullable=False)
    auth_provider = db.Column(db.String(255), nullable=False)
    member_type = db.Column(db.String(30))
    CompanyID = db.Column(db.Integer)

    def __init__(self, user_uuid, name, email, auth_provider, member_type, CompanyID):
        self.user_uuid = user_uuid
        self.name = name
        self.email = email
        self.auth_provider = auth_provider
        self.member_type = member_type
        self.CompanyID = CompanyID

    def json(self):
        return {
            "user_uuid": self.user_uuid,
            "name": self.name,
            "email": self.email,
            "auth_provider": self.auth_provider,
            "member_type": self.member_type,
            "CompanyID": self.CompanyID,
        }

################################
# GET user details with UserID #
################################


@app.route("/v1/user/get_user_by_id/<string:user_uuid>")
def get_user_by_UUID(user_uuid):
    user = User.query.filter_by(user_uuid=user_uuid).first()
    if user:
        return jsonify(
            {
                "code": 200,
                "data": user.json()
            }
        )
    return jsonify(
        {
            "code": 404,
            "message": "No user found"
        }
    )

#######################################
# Create new user account with UserID #
#######################################

# Call the api from frontend to push the data retrieved from firebase to local db
# // emit event
# const data = {
#     email: this.email,
#     firstName: this.firstName,
#     lastName: this.lastName,
#     studentOrCompany: this.accType,
#     companyName: this.companyName,
# };
# axios.post(
#     `http://127.0.0.1:8000/user/${credential.user.uid}`,
#     data
# );

@app.route("/v1/user/create_user/<string:user_uuid>/<string:email>", methods=["POST"])
def create_user_by_user_uuid(user_uuid, email):

    user_details = User.query.filter_by(email=email).first()

    data = request.get_json()
    user = User(user_uuid, **data)

    try:
        if not user_details:
            db.session.add(user)
            db.session.commit()
        else:
            return jsonify(
                {
                    "code": 500,
                    "message": "Email address have been used! Please try using another email address."
                }
            )
    except:
        return jsonify(
            {
                "code": 500,
                "data": {
                    "user_uuid": user_uuid
                },
                "message": "An error occurred creating the account."
            }
        ), 500

    return jsonify(
        {
            "code": 200,
            "data": user.json()
        }
    ), 200

##################################################################
# Upload of file, receiving URL from file upload MS through UI #
##################################################################


# @app.route("/userFile/<string:UUID>", methods=["PATCH"])
# def update_user_fileURL_by_UUID(UUID):

#     user = User.query.filter_by(UUID=UUID).first()

#     if not user:
#         return jsonify(
#             {
#                 "code": 500,
#                 "message": "User not found"
#             }
#         )

#     # {url: https://s3.amazonaws.com/esd/resume.pdf}
#     data = request.get_json()
#     user.file = data['url']

#     try:
#         db.session.commit()
#     except:
#         return jsonify(
#             {
#                 "code": 501,
#                 "message": "An error occurred while updating file."
#             }
#         ), 501

#     return jsonify(
#         {
#             "code": 200,
#             "data": user.json()
#         }
#     ), 200

################################
# User updates account details #
################################


@app.route("/v1/user/update_user_details/<string:user_uuid>", methods=["PATCH"])
def update_user_details(user_uuid):

    user = User.query.filter_by(user_uuid=user_uuid).first()

    if not user:
        return jsonify(
            {
                "code": 500,
                "message": "User not found"
            }
        )

    data = request.get_json()

    user.name = data["name"]
    user.email = data["email"]

    try:
        db.session.commit()
    except:
        return jsonify(
            {
                "code": 501,
                "data": {
                    "user_uuid": user_uuid
                },
                "message": "An error occurred while updating the account."
            }
        ), 501

    return jsonify(
        {
            "code": 200,
            "data": user.json()
        }
    ), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5008, debug=True)
