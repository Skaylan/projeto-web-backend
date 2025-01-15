from app.extensions import ma
from app.models.tables.session import Session


class SessionSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Session
        load_instance = True