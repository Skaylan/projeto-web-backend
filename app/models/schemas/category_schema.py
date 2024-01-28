from app.config.app_config import *
from app.config.db_config import *
from app.models.tables.category import Category


class CategorySchema(ma.SQLAlchemyAutoSchema):
    class Meta: 
        model = Category 
        load_instance = True
