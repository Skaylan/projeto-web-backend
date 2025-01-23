from app.extensions import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship, backref
from sqlalchemy import String, ForeignKey
from uuid import uuid4
from app.models.tables.movie_category import MovieCategory


class Category(Base):
    id: Mapped[str] = mapped_column(String, primary_key=True, default=lambda: str(uuid4()))
    name: Mapped[str] = mapped_column(String(45), unique=True, nullable=False)
    categories = relationship('MovieCategory', backref='category')
    
    def __init__(self, name:str):
        self.name = name
