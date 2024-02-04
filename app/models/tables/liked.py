from app.config.app_config import *
from app.config.db_config import *
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, ForeignKey
from uuid import uuid4, UUID 

class Liked(Base):
    id: Mapped[str] = mapped_column(String, primary_key=True, default=lambda: str(uuid4())) 
    user_id: Mapped[str] = mapped_column(String, ForeignKey("user.id"), unique=False, nullable=True)
    movie_id: Mapped[str] = mapped_column(String, ForeignKey("movie.id"), unique=False, nullable=True)

    def __init__(self, user_id: UUID, movie_id: UUID):
       self.user_id = user_id
       self.movie_id = movie_id