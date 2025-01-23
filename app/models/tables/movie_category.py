from datetime import datetime
from app.extensions import Base
from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship ,Mapped, mapped_column

class MovieCategory(Base):

    movie_id: Mapped[str] = mapped_column(String, ForeignKey("movie.id"), primary_key=True, unique=False, nullable=True)
    category_id: Mapped[str] = mapped_column(String, ForeignKey("category.id"), primary_key=True, unique=False, nullable=True)