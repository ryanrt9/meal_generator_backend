from flask import Blueprint, request, jsonify, make_response, abort
import requests
from app import db
from app.models.recipe import Recipe
from app.models.user import User
from .user_routes import validate_model
import os

recipe_bp= Blueprint('recipes', __name__, url_prefix='/search_recipes')

@recipe_bp.route("", methods=["GET"]) 
def get_recipes_by_ingredients():


    api_key=os.environ.get('SPOON_KEY')
    
    ingredients=request.args.get('ingredients') 
    

    avail_recipes= requests.get(
        f"https://api.spoonacular.com/recipes/findByIngredients?apiKey={api_key}&ingredients={ingredients}")

    all_recipes=[]

    for r in avail_recipes.json():
        new_recipe={}

        new_recipe["recipe_id"] = r["id"]
        new_recipe["image"] = r["image"]
        new_recipe["title"] = r["title"]

        all_recipes.append(new_recipe)

    for recipe in all_recipes:
        recipe_url= requests.get(
            f"https://api.spoonacular.com/recipes/{recipe['recipe_id']}/information?apiKey={api_key}"
        ).json()

        recipe["recipe_url"] = recipe_url["sourceUrl"]
        recipe["time"] = recipe_url["readyInMinutes"]
        recipe["servings"] = recipe_url["servings"]


    return make_response(jsonify(all_recipes))

@recipe_bp.route("/random", methods=["GET"])

def get_random_recipes():

    api_key=os.environ.get('SPOON_KEY')
    number=5

    response = requests.get(f"https://api.spoonacular.com/recipes/random?apiKey={api_key}&number={number}").json()

    random_recipes = []

    for i in range(number):
        random_recipe = {
            "title": response["recipes"][i]["title"],
            "recipe_id" : response["recipes"][i]["id"],
            "image" : response["recipes"][i]["image"],
            "recipe_url" : response["recipes"][i]["sourceUrl"],
            "time" : response["recipes"][i]["readyInMinutes"],
            "servings" : response["recipes"][i]["servings"]
        }

        random_recipes.append(random_recipe)

    return make_response(jsonify(random_recipes))


@recipe_bp.route("remove/<recipe_id>", methods=["DELETE"])
def delete_recipe(recipe_id):
    recipe = validate_model(Recipe, recipe_id)

    db.session.delete(recipe)
    db.session.commit()

    return {
        "details": f'Recipe {recipe.recipe_id} successfully deleted'
    }