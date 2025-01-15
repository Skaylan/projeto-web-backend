from app.extensions import ma
from app.models.tables.session import Session
from app.models.tables.user import User


class SessionSchema(ma.SQLAlchemyAutoSchema):

    users = ma.Nestad(User)
    class Meta:
        model = Session
        load_instance = True