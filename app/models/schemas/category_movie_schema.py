from app.extensions import ma
from app.models.tables.movie_category import MovieCategory
from app.models.tables.category import Category
from app.models.schemas.category_schema import CategorySchema

class MovieCategorySchema(ma.SQLAlchemyAutoSchema):
    
    Category = ma.Nested(CategorySchema)

    class Meta:
        model = MovieCategory
        load_instance = True