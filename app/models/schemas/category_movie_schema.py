from app.extensions import ma
from app.models.tables.movie_category import MovieCategory
from app.models.schemas.category_schema import CategorySchema
from app.models.schemas.movie_schema import MovieSchema


class MovieCategorySchema(ma.SQLAlchemyAutoSchema):
    movie = ma.Nested(MovieSchema)
    category = ma.Nested(CategorySchema)
    class Meta:
        model = MovieCategory
        load_instance = True