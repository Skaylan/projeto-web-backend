from app import app
from dotenv import load_dotenv
import os
from flask_cors import CORS

load_dotenv()
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URI')
CORS(app)