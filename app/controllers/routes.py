import os
import sys
from app import app
from flask import jsonify, request
from app.config.db_config import *
from app.config.app_config import *
from app.models.tables.user import User
from app.models.tables.movie import Movie
from app.models.tables.category import Category
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


@app.route('/api/v1/add_movie', methods=['POST'])
def add_movie():
    if request.method == 'POST':
        try:
            body = request.get_json()
            title = body.get('title')
            original_title = body.get('original_title')
            romanized_original_title = body.get('romanized_original_title')
            description = body.get('description')
            studio = body.get('studio')
            director = body.get('director')
            producer = body.get('producer')
            rating = body.get('rating')
            banner_img_id = body.get('banner_img_id')
            poster_img_id = body.get('poster_img_id')
            launch_date = body.get('launch_date')
            running_time = body.get('running_time')
            category_id = body.get('category_id')
            
            movie = Movie(
                title=title, original_title=original_title,
                romanised_original_title=romanized_original_title,
                description=description, studio=studio,
                director=director, producer=producer,
                rating=rating, banner_img_id=banner_img_id,
                poster_img_id=poster_img_id, launch_date=launch_date,
                running_time=running_time, category_id=category_id
            )
            
            db.session.add(movie)
            db.session.commit()
            db.session.close()
            
            return jsonify({
                'status': 'ok',
                'message': 'filme adicionado com sucesso!'
            }),201
            
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
        
    
@app.route('/api/v1/get_movies', methods=['GET'])
def get_movies():
    if request.method == 'GET':
        try:
            movies = Movie.query.all()
            movies_schema = MovieSchema(many=True)
            payload = movies_schema.dump(movies)

            return jsonify({
                'movies': payload
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
        

@app.route('/api/v1/get_one_movie', methods=['GET'])
def get_one_movie():
    if request.method == 'GET':
        try:
            title = request.args.get('title')
            studio = request.args.get('studio')

            if title != None and studio != None:
                movie = Movie.query.filter_by(title=title).filter_by(studio=studio).first()
                
                if movie == None:
                    return jsonify({
                        'status': 'error',
                        'message': 'Filme não encontrado!'
                    }),404

                movie_schema = MovieSchema()
                payload = movie_schema.dump(movie)

                return jsonify({
                    'status': 'ok',
                    'movie': payload
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
        

@app.route('/api/v1/delete_movie', methods=['DELETE'])
def delete_movie():
    try:
        if request.method == 'DELETE':

            body = request.get_json()
            id = body.get('id')

            movie = Movie.query.filter_by(id=id).first()

            if movie == None:
                return jsonify({
                    'status': 'error',
                    'massage': 'Filme não encontrado!'
                }),404
            
            db.session.delete(movie)
            db.session.commit()
            db.session.close()

            return jsonify({
                'status': 'ok',
                'message': 'Filme deletado com sucesso!'
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


@app.route('/api/v1/edit_movie', methods=['PUT'])
def edit_movie():
    if request.method == 'PUT':
        try:
            body = dict(request.get_json())
            movie_id = body.get('id')
            new_title = body.get('title')
            new_original_title = body.get('original_title')
            new_romanised_original_title = body.get('romanised_original_title')
            new_description = body.get('description')
            new_studio = body.get('studio')
            new_director = body.get('director')
            new_producer = body.get('producer')
            new_rating = body.get('rating')
            new_banner_img_id = body.get('banner_img_id')
            new_poster_img_id = body.get('poster_img_id')
            new_launch_date = body.get('launch_date')
            new_running_time = body.get('running_time')
            new_category_id = body.get('category_id')

            movie = Movie.query.filter_by(id=movie_id).first()

            if movie == None:
                return jsonify({
                    'status': 'error',
                    'message': 'Filme não encontrado'
                }), 404
            
            movie.title = new_title
            movie.original_title = new_original_title
            movie.romanised_original_title = new_romanised_original_title
            movie.description = new_description
            movie.studio = new_studio
            movie.director = new_director
            movie.producer = new_producer
            movie.rating = new_rating
            movie.banner_img_id = new_banner_img_id
            movie.poster_img_id = new_poster_img_id
            movie.launch_date = new_launch_date
            movie.running_time = new_running_time
            movie.category_id = new_category_id

            db.session.commit()
            db.session.close()

            return jsonify({
                'status': 'ok',
                'message': 'Categoria modificada com sucesso'
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
                }),500