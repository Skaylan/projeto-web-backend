import os
import sys
from app import app
from flask import jsonify, request
from app.config.db_config import *
from app.config.app_config import *
from app.models.tables.user import User
from app.models.tables.category import Category
from app.models.tables.movie import Movie
from app.models.schemas.user_schema import UserSchema
from app.models.schemas.category_schema import CategorySchema
from app.models.schemas.movie_schema import MovieSchema
from werkzeug.security import generate_password_hash, check_password_hash
import jwt


@app.route('/api/v1/get_users', methods=["GET"])
def get_users():
    try:
        users = User.query.all()
        user_schema = UserSchema(many=True)
        payload = user_schema.dump(users)
        
        return jsonify({
            'users': payload
        }), 200
        
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

@app.route('/api/v1/get_one_user', methods=['GET'])
def get_one_user():
    try:
        username = request.args.get('username')
        user = User.query.filter_by(username=username).first()
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
            

@app.route('/api/v1/delete_user', methods=['DELETE'])
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
                db.session.delete(user)
                db.session.commit()            
                db.session.close()            

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

@app.route('/api/v1/add_category', methods=['POST'])
def add_category():
    if request.method == 'POST':
        try:
            body = dict(request.get_json())
            name = body['name'] 

            category = Category(name=name)
            db.session.add(category)
            db.session.commit()
            db.session.close()      
            
            return jsonify({
                'status': 'ok',
                'message': 'Categoria adicionada com sucesso!'
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
    

@app.route('/api/v1/get_categories', methods=["GET"])
def get_categories():
    try:
        categories = Category.query.all()
        category_schema = CategorySchema(many=True)
        payload = category_schema.dump(categories)
        
        return jsonify({
            'categories': payload
        }), 200
        
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


@app.route('/api/v1/edit_category', methods=['PUT'])
def edit_category():
    if request.method == 'PUT':
        try:
            body = dict(request.get_json())
            category_id = body.get('category_id')
            new_name = body.get('new_name')

            if not category_id or not new_name:
                return jsonify({
                    'status': 'error',
                    'message': 'ID da categoria ou novo nome não foram fornecidos'
                }), 400

            category = Category.query.filter_by(id=category_id).first()

            if not category:
                return jsonify({
                    'status': 'error',
                    'message': 'Categoria não foi encontrada'
                }), 404

            category.name = new_name
            db.session.add(category)
            db.session.commit() 
            db.session.close()

            return jsonify({
                'status': 'ok',
                'message': 'Categoria modificada com sucesso'
            }), 200

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


@app.route('/api/v1/authenticate', methods=['POST'])
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
                
                return jsonify({
                    'status': 'ok',
                    'message': 'usuario autenticado com sucesso!',
                    'token': auth_token
                }), 200
                
            else:
                return jsonify({
                    "status": 'error',
                    'message': 'Senha incorreta!'
                }), 400
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
                
        

@app.route('/api/v1/delete_category', methods=['DELETE'])
def delete_category():
    if request.method == 'DELETE':
        try:
            body = request.get_json()
            id = body.get('id')

            category = Category.query.filter_by(id=id).first()

            if category == None:
                return jsonify({
                    'status': 'error',
                    'message': 'Categoria não encotrada'
                }),404
            
            db.session.delete(category)
            db.session.commit()
            db.session.close()

            return jsonify({
                'status': 'ok',
                'message': 'Categoria deletada com sucesso!'
            }),200

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
        

@app.route('/api/v1/get_one_category', methods=['GET'])
def get_one_category():
    if request.method == 'GET':
        try:
            name = request.args.get('name')

            one_category = Category.query.filter_by(name=name).first()

            if one_category == None:
                return jsonify({
                    'status': 'error',
                    'message': 'Categoria não encontrada!'
                }),404
            
            category_schema = CategorySchema()
            payload = category_schema.dump(one_category)

            return jsonify({
                'status': 'ok',
                'category': payload
            }),200
        
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
        
    
@app.route('/api/v1/get_movies')
def get_movies():
    try:
        movies = Movie.query.all()
        movies_schema = MovieSchema(many=True)
        payload = movies_schema.dump(movies)

        return jsonify({
            'movies': payload
        }),200

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


