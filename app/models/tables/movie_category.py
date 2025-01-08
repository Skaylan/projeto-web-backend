from app.extensions import Base
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, ForeignKey
from uuid import uuid4 


class MovieCategory(Base):
    id: Mapped[str] = mapped_column(String, primary_key=True, default=lambda: str(uuid4()))
    movie_id: Mapped[str] = mapped_column(String, ForeignKey('movie.id'), nullable=False)
    category_id: Mapped[str] = mapped_column(String, ForeignKey('category.id'), nullable=False)
    
    def __init__(self, movie_id: str, category_id: str):
        self.category_id = category_id
        self.movie_id = movie_id
        