from flask import Blueprint, request, jsonify, make_response, abort
import requests
from app import db
from app.models.recipe import Recipe
from app.models.user import User
import os

user_bp= Blueprint('user', __name__, url_prefix='/')

# post request to create a user
@user_bp.route("signup", methods=["POST"])
def create_user():
    request_body = request.get_json()

    if "email" not in request_body:
        return make_response({ "error message" :
            "Invalid data. Must include email"
        }, 400)
    if "password" not in request_body:
        return make_response({"error message" :
            "Invalid data. Must include password"
        }, 400)

    new_user = User(
        email=request_body["email"], 
        password=request_body["password"]
    )

    db.session.add(new_user)
    db.session.commit()
    
    return make_response({"user":new_user.to_dict()}, 201)

# get is to log in
@user_bp.route("/<user_id>", methods=["GET"])
def get_one_user(user_id):
    # user = validate_user(user_id)
    user = User.query.get(user_id)
    
    return {"user": user.to_dict()}

# user can delete profile
@user_bp.route("/<user_id>", methods=["DELETE"])
def delete_one_board(user_id):
    user = User.query.get(user_id)

    db.session.delete(user)
    db.session.commit()

    return make_response({"message": "User successfully deleted"}, 200)
