import os
from flask import jsonify, request, Blueprint
from app.models.tables.user import User
from app.models.tables.session import Session
from app.controllers.utils.functions import print_error_details
from werkzeug.security import check_password_hash
from app.extensions import db
import jwt


auth_route = Blueprint('auth_route', __name__)

@auth_route.route('/api/v1/authenticate', methods=['POST'])
def authenticate():
    if request.method == 'POST':
        try:
            body = request.get_json()
            email = body.get('email')
            password = body.get('password')
                    
            user = User.query.filter_by(email=email).first()
            
            if user == None:
                return jsonify({
                    'status': 'error',
                    'message': f'usuario com email {email} não existe!'
                }), 404
            
            checked_pass = check_password_hash(user.password_hash, password)
            
            if checked_pass:
                secret_key = os.getenv('SECRET_KEY')
                auth_token = jwt.encode({'email': user.email, 'user_id': user.id}, secret_key)
                
                new_session = Session(session_token=auth_token, user_id=user.id)
                db.session.add(new_session)
                db.session.commit()
                
                return jsonify({
                    'status': 'ok',
                    'message': 'usuario autenticado com sucesso!',
                    'token': auth_token,
                }), 200
                
            else:
                return jsonify({
                    "status": 'error',
                    'message': 'Senha incorreta!'
                }), 400
        except Exception as error:
            print_error_details(error)
            return jsonify({
                'status': 'error',
                'message': 'An error has occurred!',
                'error_class': str(error.__class__),
                'error_cause': str(error.__cause__)
            }), 500
                

@auth_route.route('/api/v1/logout', methods=['POST'])
def logout():
    if request.method == 'POST':
        try:
            body = request.get_json()

            if 'token' not in body:
                return jsonify({
                    'status': 'error',
                    'message': 'Token de autorização ausente!'
                }), 401

            token = body.get('token')
            session = Session.query.filter_by(session_token=token).first()

            if session is None:
                return jsonify({
                    'status': 'error',
                    'message': 'Token de sessão inválido!'
                }), 401

            db.session.delete(session)
            db.session.commit()

            return jsonify({
                'status': 'ok',
                'message': 'Usuário desconectado com sucesso!'
            }), 200

        except Exception as error:
            print_error_details(error)
            return jsonify({
                'status': 'error',
                'message': 'Ocorreu um erro!',
                'error_class': str(error.__class__),
                'error_cause': str(error.__cause__)
            }), 500