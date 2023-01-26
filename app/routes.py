from flask import Blueprint, request, jsonify, make_response, abort
from app import db
# from app.models.user import User
# from app.models.recipe import Recipe

# # example_bp = Blueprint('example_bp', __name__)
# board_bp = Blueprint('user_bp', __name__, url_prefix='/user')

# # non-route functions
# def validate_user(user_id):
#     try:
#         user_id = int(user_id)
#     except:
#         abort(make_response({"error message":f"User {user_id} invalid"}, 400))

#     user = User.query.get(user_id)

#     if not user:
#         abort(make_response({"error message":f"User {user_id} not found"}, 404))