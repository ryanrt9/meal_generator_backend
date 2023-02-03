from flask import Blueprint, request, jsonify, make_response, abort
import requests
from app import db
from app.models.recipe import Recipe
from app.models.user import User
import os

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

# post request to create a user
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
    
    return make_response({"user_created":new_user.to_dict()}, 201)

# get is to log in
@user_bp.route("/<user_id>", methods=["GET"])
def get_one_user(user_id):
    # user = validate_user(user_id)
    user = validate_model(User, user_id)
    
    return {"user": user.to_dict()}
    # return make_response({"message": f"User {user_id} successfully deleted"}, 200)

# user can delete profile
@user_bp.route("/<user_id>", methods=["DELETE"])
def delete_one_board(user_id):
    user = User.query.get(user_id)

    db.session.delete(user)
    db.session.commit()

    return {"user_deleted": user.to_dict()}


# ---------------------Nested Routes ------------------------------ 

# "user/recipes"
# get all recipes by user id -> this is what will be rendered to the saved recipes page
@user_bp.route("/<user_id>/recipes", methods=["GET"])

def get_all_recipes_by_user_id(user_id):
    user = validate_model(User,user_id)

    return_body = user.to_dict()
    return_body = [recipe.to_dict() for recipe in user.recipes]

    return make_response(jsonify(return_body), 200)


# add a new recipe to user id -> post request made to our backend model
@user_bp.route("/<user_id>/add_recipe", methods=["POST"])
def add_recipe_to_user(user_id):   
    user = validate_model(User, user_id)
    
    request_body = request.get_json()
    try:
        add_recipe= Recipe.from_dict(request_body) 
        # the request body info is coming from the component 
        
    except KeyError:
        return {"details": "Missing Data"}, 400
    
    db.session.add(add_recipe)
    db.session.commit()

    # return add_recipe.to_dict(), 201
    # return make_response(jsonify({f'Recipe: {add_recipe.title} has been successfully deleted!'}), 200)
    return add_recipe.to_dict(), 201