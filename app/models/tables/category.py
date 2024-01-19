from app.config.app_config import *
from app.config.db_config import *
from datetime import datetime

class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(45), unique=True, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DataTime, default=datetime.utcnow, onupdate=datetime.utcnow)
  
    def __init__(
        self,
        nome: str,
    ) :
        self.nome = nome
   
    



