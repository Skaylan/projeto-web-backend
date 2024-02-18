from app.extensions import ma
from app.models.tables.category import Category


class CategorySchema(ma.SQLAlchemyAutoSchema):
    class Meta: 
        model = Category 
        load_instance = True
