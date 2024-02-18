from app.extensions import ma
from app.models.tables.user import User


class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = User
        load_instance = True
        exclude=['password_hash']