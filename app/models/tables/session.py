from app.extensions import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Integer, Text, ForeignKey, String
from uuid import uuid4


class Session(Base):
    id: Mapped[str] = mapped_column(String, primary_key=True, default=lambda: str(uuid4()))
    session_token: Mapped[str] = mapped_column(Text, nullable=False, unique=True)
    user_id: Mapped[str] = mapped_column(String, ForeignKey('user.id'), nullable=False)
    user = relationship('User', backref='sessions')

    def __init__(self, session_token: str, user_id: int):
        self.session_token = session_token
        self.user_id = user_id
