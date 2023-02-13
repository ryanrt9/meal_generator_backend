from flask import Blueprint, request, jsonify, make_response, abort
import requests
from app import db
from app.models.recipe import Recipe
from app.models.user import User
import os
import uuid

user_bp= Blueprint('user', __name__, url_prefix='/user')

def validate_model(cls, model_id):
    try:
        model_id = int(model_id)
    except:
        abort(make_response({"message": f"{cls.__name__} {model_id} invalid, id must be a number"}, 400))
    
    model = cls.query.get(model_id)
    if not model:
        abort(make_response({"message": f"There is no existing {cls.__name__} {model_id}"}, 404))
    
    return model

def generate_session_token():
    return str(uuid.uuid4())


@user_bp.route("/signup", methods=["POST"])
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

    token = generate_session_token()
    
    return jsonify({"token":token})

@user_bp.route("/login", methods=["POST"])
def login_user():

    email = request.json.get("email")
    password = request.json.get("password")

    users = User.query.all()

    all_users = [user.to_dict() for user in users]

    user_email= next((u for u in all_users if u['email'] == email), None)
    user_password = next((u for u in all_users if u['password'] == password), None)

    if not user_email or not user_password:
        return jsonify({'error': 'email or password is incorrect'}), 400


    token = generate_session_token()

    return jsonify({"token":token})

@user_bp.route("/all_users", methods=["GET"])
def get_all_users():
    users= User.query.all()

    users_response = [user.to_dict() for user in users]
    
    return (jsonify(users_response))


@user_bp.route("/<user_id>", methods=["DELETE"])
def delete_one_board(user_id):
    user = User.query.get(user_id)

    db.session.delete(user)
    db.session.commit()

    return {"user_deleted": user.to_dict()}


# ---------------------Nested Routes ------------------------------ 

@user_bp.route("/<user_id>/recipes", methods=["GET"])

def get_all_recipes_by_user_id(user_id):
    user = validate_model(User,user_id)

    return_body = user.to_dict()
    return_body = [recipe.to_dict() for recipe in user.recipes]

    return make_response(jsonify(return_body), 200)


@user_bp.route("/<user_id>/add_recipe", methods=["POST"])
def add_recipe_to_user(user_id):   
    user = validate_model(User, user_id)
    
    request_body = request.get_json()
    try:
        add_recipe= Recipe.from_dict(request_body) 
        
    except KeyError:
        return {"details": "Missing Data"}, 400
    
    db.session.add(add_recipe)
    db.session.commit()

    return add_recipe.to_dict(), 201