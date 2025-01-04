from app.extensions import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship, backref
from sqlalchemy import String, ForeignKey
from uuid import uuid4


class Category(Base):
    id: Mapped[str] = mapped_column(String, primary_key=True, default=lambda: str(uuid4()))
    name: Mapped[str] = mapped_column(String(45), unique=True, nullable=False)
    movie_id: Mapped[str] = mapped_column(String, ForeignKey("movie.id"), nullable=False)
    
    def __init__(self, name:str, movie_id: str):
        self.name = name
        self.movie_id = movie_id
