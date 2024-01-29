from app.config.app_config import *
from app.config.db_config import *
from app.models.tables.movie import Movie
from app.models.schemas.category_schema import CategorySchema


class MovieSchema(ma.SQLAlchemyAutoSchema):
    category = ma.Nested(CategorySchema)
    class Meta:
        model = Movie
        load_instance = True