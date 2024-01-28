from app.config.app_config import *
from app.config.db_config import *
from app.models.tables.movie import Movie
from datetime import datetime
from sqlalchemy.orm import Mapped, mapped_column, relationship, backref
from sqlalchemy import String, Integer, DateTime, Text
from uuid import uuid4


class Category(db.Model):
    id: Mapped[str] = mapped_column(String, primary_key=True, default=lambda: str(uuid4()))
    name: Mapped[str] = mapped_column(String(45), unique=True, nullable=False)
    created_at: Mapped[DateTime] = mapped_column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at: Mapped[DateTime] = mapped_column(DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)

    movies = relationship('Movie', backref='category') 
    
    def __init__(self, name:str):
        self.name = name
