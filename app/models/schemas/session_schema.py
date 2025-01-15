from app.extensions import ma
from app.models.tables.session import Session
#from app.models.schemas.user_schema import UserSchema
from app.models.tables.user import User

class SessionSchema(ma.SQLAlchemyAutoSchema):

    user = ma.Nested(User)
    class Meta:
        model = Session
        load_instance = True