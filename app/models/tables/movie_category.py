from app.extensions import db
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, ForeignKey
from uuid import uuid4 


movie_category = db.Table('movie_category',
    db.Column('movie_id', String, db.ForeignKey('movie.id'), primary_key=True),
    db.Column('category_id', String, db.ForeignKey('category.id'), primary_key=True)
)