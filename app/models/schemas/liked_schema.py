from app.extensions import ma
from app.models.tables.liked import Liked
from app.models.schemas.user_schema import UserSchema
from app.models.schemas.movie_schema import MovieSchema

class LikedSchema(ma.SQLAlchemyAutoSchema):
    user = ma.Nested(UserSchema)
    movie = ma.Nested(MovieSchema)
    class Meta:
        model = Liked
        load_instance = True