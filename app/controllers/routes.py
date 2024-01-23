import sys
from app import app
from flask import jsonify, request
from app.config.db_config import *
from app.config.app_config import *
from app.models.tables.user import User
from app.models.tables.category import Category
from app.models.schemas.user_schema import UserSchema
from werkzeug.security import generate_password_hash, check_password_hash


@app.route('/api/v1/get_users', methods=["GET"])
def get_users():
    users = User.query.all()
    user_schema = UserSchema(many=True)
    payload = user_schema.dump(users)
    
    return jsonify({
        'users': payload
    }), 200
    
    
@app.route('/api/v1/create_user', methods=['POST'])
def create_user():
    if request.method == 'POST':
        try:
            body = dict(request.get_json())
            name = body['name']
            username = body['username']
            email = body['email']
            password = body['password']
            re_password = body['re_password']
            
            
            if password != re_password:
                return jsonify({
                    'status': 'error',
                    "message": 'Senhas não coencidem'
                }), 400
            
            password_hash = generate_password_hash(password)
                        
            user = User(name=name, username=username, email=email, password_hash=password_hash)
            db.session.add(user)
            db.session.commit()
            
            return jsonify({
                'status': 'ok',
                'message': 'Usuario criado com sucesso!'
            }), 201
            
        except Exception as error:
            print(f'error class: {error.__class__} | error cause: {error.__cause__}')
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)
            return jsonify({
                    'status': 'error',
                    'message': 'An error has occurred!',
                    'error_class': str(error.__class__),
                    'error_cause': str(error.__cause__)
                }), 500
            