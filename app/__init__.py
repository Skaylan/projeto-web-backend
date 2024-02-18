from flask import Flask
from dotenv import load_dotenv
import os
from flask_cors import CORS
from .extensions import db, migrate, ma
from app.controllers.routes.auth_routes import auth_route
from app.controllers.routes.user_routes import user_route
from app.controllers.routes.movie_routes import movie_route
from app.controllers.routes.category_routes import category_route

load_dotenv()

def create_app():
    app = Flask(__name__)

    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URI')
    CORS(app)
    
    db.init_app(app)
    migrate.init_app(app, db)
    ma.init_app(app)
    
    app.register_blueprint(auth_route)
    app.register_blueprint(user_route)
    app.register_blueprint(movie_route)
    app.register_blueprint(category_route)
    
    return app