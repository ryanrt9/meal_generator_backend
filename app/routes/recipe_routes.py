from flask import Blueprint, request, jsonify, make_response, abort
import requests
from app import db
from app.models.recipe import Recipe
from app.models.user import User
import os
# from app.routes.routes_helper import validate_model

recipe_bp= Blueprint('recipes', __name__, url_prefix='/search_recipes')

# Click 'find me recipes'
@recipe_bp.route("", methods=["GET"]) 
    # we will have to change the format from ["apples", "bananas"] -> "apples, bananas" with .join in the front end
    # the reason is because spoonacular takes in a a comma-seperated list of ingrediets of type string
def get_recipes_by_ingredients():

    # this is our API key from spoonacular
    api_key=os.environ.get('SPOON_KEY')
    # this is the query param we get from the user input in the form
    ingredients=request.args.get('ingredients')
    # here in the backend we can modify the user input to turn each ingredient into a list of strings else we will get an empty list
    ingredients_list = ingredients.split(',') if ingredients else []

    avail_recipes= requests.get(
        f"https://api.spoonacular.com/recipes/findByIngredients?apiKey={api_key}&ingredients={','.join(ingredients_list)}")

    all_recipes=[]

    for r in avail_recipes.json():
        new_recipe={}

        new_recipe["recipe_id"] = r["id"]
        new_recipe["image"] = r["image"]
        new_recipe["title"] = r["title"]

        all_recipes.append(new_recipe)

    # now that I have the id, i can call "get recipe information" to pull out the URL and add it to the dict we made
    for recipe in all_recipes:
        recipe_url= requests.get(
            f"https://api.spoonacular.com/recipes/{recipe['recipe_id']}/information?apiKey={api_key}"
        ).json()

        recipe["recipe_url"] = recipe_url["sourceUrl"]
        recipe["time"] = recipe_url["readyInMinutes"]


    return make_response(jsonify(all_recipes))

@recipe_bp.route("/random", methods=["GET"])

def get_random_recipes():
    random_recipes = []

    random_recipe={}
    api_key=os.environ.get('SPOON_KEY')
    number=5

    response = requests.get(f"https://api.spoonacular.com/recipes/random?apiKey={api_key}&number={number}").json()

    for i in range(number):
        random_recipe["title"] = response["recipes"][i]["title"]
        random_recipe["recipe_id"] = response["recipes"][i]["id"]
        random_recipe["image"] = response["recipes"][i]["image"]
        random_recipe["recipe_url"] = response["recipes"][i]["sourceUrl"]
        random_recipe["time"] = response["recipes"][i]["readyInMinutes"]

        random_recipes.append(random_recipe)

    return make_response(jsonify(random_recipes))


    # ---------------------Nested Routes ------------------------------ 

# To Do
# - check if our models look good
# - test our User routes
# - Write nested routes ->will be used for users that are signed in (check yellow/red blocks in notion)
# - Deploy on Heroku!
    #- and then Front End will be on Google Firebase?