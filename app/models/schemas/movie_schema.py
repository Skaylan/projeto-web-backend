from app.extensions import ma
from app.models.tables.movie import Movie
from app.models.schemas.category_schema import CategorySchema


class MovieSchema(ma.SQLAlchemyAutoSchema):
    category = ma.Nested(CategorySchema)
    class Meta:
        model = Movie
        load_instance = True