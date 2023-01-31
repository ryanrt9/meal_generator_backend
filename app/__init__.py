from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from dotenv import load_dotenv
import os
from flask_cors import CORS

db = SQLAlchemy()
migrate = Migrate()
load_dotenv()


def create_app(test_config=None):
    app = Flask(__name__)


    CORS(app)
    app.config['CORS_HEADERS'] = 'Content-Type'
    
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    app.config["SQLALCHEMY_DATABASE_URI"] = 'postgresql+psycopg2://postgres:postgres@localhost:5432/meal_generator_development'

    # Import models here for Alembic setup
    # from app.models.ExampleModel import ExampleModel
    from app.models.user import User
    from app.models.recipe import Recipe

    db.init_app(app)
    migrate.init_app(app, db)

    # Register Blueprints here
    # from .routes import example_bp
    # app.register_blueprint(example_bp)
    # from .user_routes import user_bp
    # app.register_blueprint(user_bp)

    # from .recipe_routes import recipe_bp
    # app.register_blueprint(recipe_bp)

    return app
