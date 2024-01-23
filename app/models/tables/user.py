from app.config.app_config import *
from app.config.db_config import *
from datetime import datetime
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Integer, DateTime, Text
from uuid import uuid4


class User(db.Model):
    id: Mapped[str] = mapped_column(String, primary_key=True, default=str(uuid4()))
    name: Mapped[str] = mapped_column(String(100), unique=False, nullable=False)
    username: Mapped[str] = mapped_column(String(20), unique=True, nullable=False)
    email: Mapped[str] = mapped_column(String(320), unique=True, nullable=False)
    password_hash: Mapped[str] = mapped_column(Text, unique=False, nullable=False)
    created_at: Mapped[DateTime] = mapped_column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at: Mapped[DateTime] = mapped_column(DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __init__(self, name:str, username:str, email:str, password_hash:str):
        self.name = name
        self.username = username
        self.email = email
        self.password_hash = password_hash
