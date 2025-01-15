from app.extensions import ma
from app.models.tables.user import User
from app.models.schemas.session_schema import Session


class UserSchema(ma.SQLAlchemyAutoSchema):
    session = ma.Nested(Session)
    class Meta:
        model = User
        load_instance = True
        exclude=['password_hash']