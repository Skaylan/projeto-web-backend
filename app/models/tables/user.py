from app.config.app_config import *
from app.config.db_config import *
from datetime import datetime

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), unique=False, nullable=False)
    username = db.Column(db.String(100), unique=False, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password_hash = db.Column(db.Text, unique=False, nullable=False)
    created_at = db.Column(db.DataTime, defaut=datetime.now())
    updated_at = db.Column(db.DataTime, defaut=datetime.now())