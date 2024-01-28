from app.config.app_config import *
from app.config.db_config import *
from app.models.tables.movie import Movie


class MovieSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Movie
        load_instance = True