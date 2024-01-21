from app import app
from app.config.db_config import *
from app.config.app_config import *
from flask import jsonify
from app.models.schema.user_schema import UserSchema
from app.models.tables.user import User
from app.models.tables.category import Category


@app.route('/api/v1/get_users', methods=["GET"])
def get_users():
    users = User.query.all()
    user_schema = UserSchema(many=True)
    payload = user_schema.dump(users)
    
    return jsonify({
        'users': payload
    }), 200