from app.config.app_config import *
from app.config.db_config import *
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Text, Integer, Double, ForeignKey
from uuid import uuid4 

class Movie(Base): 
    id: Mapped[str] = mapped_column(String, primary_key=True, default=lambda: str(uuid4())) 
    title: Mapped[str] = mapped_column(Text, unique=False, nullable=False)
    original_title: Mapped[str] = mapped_column(Text, unique=False, nullable=False)
    romanised_original_title: Mapped[str] = mapped_column(Text, unique=False, nullable=False)
    description: Mapped[str] = mapped_column(Text, unique=False, nullable=False) 
    studio: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    director: Mapped[str] = mapped_column(String(100), unique=False, nullable=False)
    producer: Mapped[str] = mapped_column(String(100), unique=False, nullable=False) 
    rating: Mapped[Double] = mapped_column(Double, unique=False, nullable=False) 
    banner_img_id: Mapped[str] = mapped_column(Text, unique=True, nullable=False) 
    poster_img_id: Mapped[str] = mapped_column(Text, unique=True, nullable=False) 
    launch_date: Mapped[str] = mapped_column(String(45), unique=False, nullable=False)
    running_time: Mapped[int] = mapped_column(Integer, unique=True, nullable=False) 
    category_id: Mapped[str] = mapped_column(String, ForeignKey("category.id"), unique=False, nullable=False) 


    def __init__(self, title: str, original_title: str, romanised_original_title: str,
                 description: str, studio: str, director: str, rating: Double,
                 banner_img_id: str, launch_date: str, cover_img_id: str, producer: str,
                 running_time: int, category_id: str
                 ):
        self.title = title
        self.original_title = original_title
        self.romanised_original_title = romanised_original_title
        self.description = description
        self.studio = studio
        self.director = director
        self.rating = rating
        self.banner_img_id = banner_img_id
        self.launch_date = launch_date
        self.cover_img_id = cover_img_id
        self.producer = producer
        self.running_time = running_time
        self.category_id = category_id