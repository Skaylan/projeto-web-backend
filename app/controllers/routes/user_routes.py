from app.extensions import db
from app.models.tables.user import User
from app.models.tables.session import Session
from flask import jsonify, request, Blueprint
from app.models.schemas.user_schema import UserSchema
from app.controllers.utils.functions import print_error_details
from werkzeug.security import generate_password_hash, check_password_hash



user_route = Blueprint('user_route', __name__)

@user_route.route('/api/v1/get_users', methods=["GET"])
def get_users():
    try:
        users = User.query.all()
        user_schema = UserSchema(many=True)
        payload = user_schema.dump(users)
        
        return jsonify({
            'users': payload
        }), 200
        
    except Exception as error:
        print_error_details(error)
        return jsonify({
                'status': 'error',
                'message': 'An error has occurred!',
                'error_class': str(error.__class__),
                'error_cause': str(error.__cause__)
            }), 500

@user_route.route('/api/v1/get_one_user', methods=['GET'])
def get_one_user():
    try:
        email = request.args.get('email')
        user = User.query.filter_by(email=email).first()
        user_schema = UserSchema()
        payload = user_schema.dump(user)
        
        if user == None:
            return jsonify({
                'status': 'error',
                'mesage': 'usuario não existe!'
            }), 404
            
        return jsonify({
            'status': 'ok',
            'user': payload
        }), 200
        
    except Exception as error:
        print_error_details(error)
        return jsonify({
                'status': 'error',
                'message': 'An error has occurred!',
                'error_class': str(error.__class__),
                'error_cause': str(error.__cause__)
            }), 500
    
    
@user_route.route('/api/v1/create_user', methods=['POST'])
def create_user():
    if request.method == 'POST':
        try:
            body = request.get_json()
            name = body['name']
            username = body['username']
            email = body['email']
            password = body['password']
            re_password = body['re_password']
            
            
            if password != re_password:
                return jsonify({
                    'status': 'error',
                    'message': 'Senhas não coencidem'
                }), 400
            
            password_hash = generate_password_hash(password)
                        
            user = User(name=name, username=username, email=email, password_hash=password_hash)
            db.session.add(user)
            db.session.commit()
            db.session.close()
            
            return jsonify({
                'status': 'ok',
                'message': 'Usuario criado com sucesso!'
            }), 201
            
        except Exception as error:
            print_error_details(error)
            return jsonify({
                    'status': 'error',
                    'message': 'An error has occurred!',
                    'error_class': str(error.__class__),
                    'error_cause': str(error.__cause__)
                }), 500
            

@user_route.route('/api/v1/delete_user', methods=['DELETE'])
def delete_user():
    if request.method == 'DELETE':
        try:
            body = dict(request.get_json())
            username = body.get('username')
            password = body.get('password')
            
            
            user = User.query.filter_by(username=username).first()

            if user == None:
                return jsonify({
                    'status': 'error',
                    'message': 'usuario não existe!'
                }), 404
            
            checked_password = check_password_hash(user.password_hash, password)
            if checked_password:
                session = Session.query.filter_by(user_id=user.id).first()
                if session != None:
                  db.session.delete(session)
                  db.session.delete(user)
                  db.session.commit()
                else:
                  db.session.delete(user)
                  db.session.commit()
                  

                return jsonify({
                    'status': 'ok',
                    'message': 'usuario deletado com sucesso!'
                }), 200
            else:
                return jsonify({
                    'status': 'error',
                    'message': 'Senha incorreta!'
                }), 401
                
        except Exception as error:
            print_error_details(error)
            return jsonify({
                    'status': 'error',
                    'message': 'An error has occurred!',
                    'error_class': str(error.__class__),
                    'error_cause': str(error.__cause__)
                }), 500
