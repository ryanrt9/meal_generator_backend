from flask import Blueprint, request, jsonify, make_response, abort
import requests
from app import db
from app.models.recipe import Recipe
from app.models.user import User
from .user_routes import validate_model
import os
# from app.routes.routes_helper import validate_model

recipe_bp= Blueprint('recipes', __name__, url_prefix='/search_recipes')

# Click 'find me recipes'
@recipe_bp.route("", methods=["GET"]) 
def get_recipes_by_ingredients():

    # this is our API key from spoonacular
    api_key=os.environ.get('SPOON_KEY')
    # this is the query param we get from the user input in the form -> input is in the form ["apple", "banana", "yogurt"]
    ingredients=request.args.get('ingredients') 
    # here in the backend we can modify the user input to turn each ingredient into a list of strings else we will get an empty list
    # ingredients_list = ingredients.split(',') if ingredients else [] 

    avail_recipes= requests.get(
        # f"https://api.spoonacular.com/recipes/findByIngredients?apiKey={api_key}&ingredients={','.join(ingredients_list)}")
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


    return make_response(jsonify(all_recipes))

@recipe_bp.route("/random", methods=["GET"])

def get_random_recipes():

    # random_recipe={}
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
            "time" : response["recipes"][i]["readyInMinutes"]
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