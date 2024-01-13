from app.config.app_config import *
from app.config.db_config import *
from app.models.tables.user import User

class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = User
        load_instance = True
        # exclude=['password_hash']