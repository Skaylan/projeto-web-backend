import os
from app import app
from flask_cors import CORS
from dotenv import load_dotenv


load_dotenv()
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URI')
CORS(app)