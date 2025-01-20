from app.extensions import Base
from app.models.tables.liked import Liked
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Text
from uuid import uuid4


class User(Base):
    id: Mapped[str] = mapped_column(Text, primary_key=True, default=lambda: str(uuid4()))
    name: Mapped[str] = mapped_column(String(100), unique=False, nullable=False)
    username: Mapped[str] = mapped_column(String(20), unique=True, nullable=False)
    email: Mapped[str] = mapped_column(String(320), unique=True, nullable=False)
    banner_img_id: Mapped[str] = mapped_column(Text, unique=True, nullable=True) 
    profile_img_id: Mapped[str] = mapped_column(Text, unique=True, nullable=True)
    password_hash: Mapped[str] = mapped_column(Text, unique=False, nullable=False)
    liked = relationship(Liked, backref='user') 
    
    def __init__(self, name:str, username:str, email:str, password_hash:str):
        self.name = name
        self.username = username
        self.email = email
        self.password_hash = password_hash

    def set_images(self, banner_img_id: str, profile_img_id: str):
        self.banner_img_id = banner_img_id
        self.profile_img_id = profile_img_id