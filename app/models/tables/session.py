from app.config.app_config import *
from app.config.db_config import *
from app.models.tables.user import User
from sqlalchemy.orm import Mapped, mapped_column, relationship, backref
from sqlalchemy import Column, Integer, Text, DateTime, ForeignKey, String
from uuid import uuid4


class Session(Base):
    id: Mapped[str] = mapped_column(String, primary_key=True, default=lambda: str(uuid4()))
    session_token: Mapped[str] = mapped_column(Text, nullable=False, unique=True)
    user_id: Mapped[str] = mapped_column(Integer, ForeignKey('user.id'), nullable=False)
    user = relationship('User', backref='sessions')

    def __init__(self, session_token: str, user_id: int):
        self.session_token = session_token
        self.user_id = user_id
