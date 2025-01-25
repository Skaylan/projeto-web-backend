from flask import jsonify, request, Blueprint
from app.models.tables.movie_category import MovieCategory
from app.models.tables.movie import Movie
from app.models.tables.liked import Liked
from app.models.tables.category import Category
from app.controllers.utils.functions import print_error_details
from app.models.schemas.movie_schema import MovieSchema
from app.models.schemas.liked_schema import LikedSchema
from app.models.schemas.category_schema import CategorySchema
from app.models.schemas.category_movie_schema import MovieCategorySchema
from app.extensions import db
from app.utils import *
from uuid import uuid4
import os
from dotenv import load_dotenv


IMG_PATH = os.getenv('IMAGES_SAVE_PATH')

movie_route = Blueprint('movie_route', __name__)

@movie_route.route('/get/v1/get_image', methods=['GET'])
def get_image():
    if request.method == 'GET':
        
        #rota apenas para teste local
        
        id_imag = 'd8c5edd6-5a03-42a8-ae9d-8375296db2f1'
        
        try:        
            string64 = convert_image_to_base64(IMG_PATH, id_imag)
            
            return jsonify({
                'img': string64
            }), 201
            
            
        except Exception as error:
            print_error_details(error)
            return jsonify({
                    'status': 'error',
                    'message': 'An error has occurred!',
                    'error_class': str(error.__class__),
                    'error_cause': str(error.__cause__)
                }), 500
            

@movie_route.route('/api/v1/add_movie', methods=['POST'])
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
            banner_img_base64 = body.get('banner_img_base64')
            poster_img_base64 = body.get('poster_img_base64')
            release_date = body.get('launch_date')
            running_time = body.get('running_time')
            categories = body.get('categories')

            banner_img_id = str(uuid4())
            poster_img_id = str(uuid4())

            convert_base64_to_image(banner_img_base64, banner_img_id, IMG_PATH)
            convert_base64_to_image(poster_img_base64, poster_img_id, IMG_PATH)

            movie = Movie(
                title=title, original_title=original_title,
                romanised_original_title=romanized_original_title,
                description=description, studio=studio,
                director=director, producer=producer,
                rating=rating, banner_img_id=banner_img_id,
                poster_img_id=poster_img_id, release_date=release_date,
                running_time=running_time
            )

            db.session.add(movie)
            db.session.flush() 
            
            for category_id in categories:
                category = Category.query.filter_by(id=category_id).first()
                print(category)
                if category:
                    movie_category = MovieCategory(movie_id=movie.id, category_id=category.id)
                    db.session.add(movie_category)
            
            db.session.commit()
                
            db.session.close()
            
            return jsonify({
                'status': 'ok',
                'message': 'filme adicionado com sucesso!'
            }),201
            
        except Exception as error:
            print_error_details(error)
            return jsonify({
                    'status': 'error',
                    'message': 'An error has occurred!',
                    'error_class': str(error.__class__),
                    'error_cause': str(error.__cause__)
                }), 500

@movie_route.route('/api/v1/get_movies', methods=['GET'])
def get_movies():
    if request.method == 'GET':
        try:
            movies = MovieCategory.query.all()
            movies_schema = MovieCategorySchema(many=True)
            payload = movies_schema.dump(movies)

            movies_by_id = {}
            for item in payload:
                movie_id = item['movie']['id']

                if movie_id not in movies_by_id:
                    movies_by_id[movie_id] = {
                        **item['movie'],
                        "categories": []
                    }

                movies_by_id[movie_id]['categories'].append(item['category'])

                if len(movies_by_id[movie_id]['categories']) == 1:
                    movies_by_id[movie_id]['banner_img'] = convert_image_to_base64(IMG_PATH, item['movie']['banner_img_id'])
                    movies_by_id[movie_id]['poster_img'] = convert_image_to_base64(IMG_PATH, item['movie']['poster_img_id'])

            movies_list = list(movies_by_id.values())

            return jsonify({
                'movies': movies_list
            }), 200

        except Exception as error:
            print_error_details(error)
            return jsonify({
                    'status': 'error',
                    'message': 'An error has occurred!',
                    'error_class': str(error.__class__),
                    'error_cause': str(error.__cause__)
                }), 500
        

@movie_route.route('/api/v1/get_one_movie', methods=['GET'])
def get_one_movie():
    if request.method == 'GET':
        try:
            title = request.args.get('title')
            studio = request.args.get('studio')
            
            if title != None and studio != None:
                movie = Movie.query.filter_by(title=title).filter_by(studio=studio).first()
                movie_category = MovieCategory.query.filter_by(movie_id=movie.id).first()
                
                if movie == None:
                    return jsonify({
                        'status': 'error',
                        'message': 'Filme não encontrado!'
                    }),404

                movie_schema = MovieCategorySchema()
                payload = movie_schema.dump(movie_category)
                
                payload['movie']['poster_img'] = convert_image_to_base64(IMG_PATH, payload['movie']['poster_img_id'])
                payload['movie']['banner_img'] = convert_image_to_base64(IMG_PATH, payload['movie']['banner_img_id'])

                return jsonify({
                    'status': 'ok',
                    'movie': payload
                }),200

        except Exception as error:
            print_error_details(error)
            return jsonify({
                'status': 'error',
                'message': 'An error has occurred!',
                'error_class': str(error.__class__),
                'error_cause': str(error.__cause__)
            }), 500
        

@movie_route.route('/api/v1/delete_movie', methods=['DELETE'])
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
        print_error_details(error)
        return jsonify({
                'status': 'error',
                'message': 'An error has occurred!',
                'error_class': str(error.__class__),
                'error_cause': str(error.__cause__)
            }), 500


@movie_route.route('/api/v1/edit_movie', methods=['PUT'])
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
            new_banner_img_base64 = body.get('banner_img_base64')
            new_poster_img_base64 = body.get('poster_img_base64')
            new_launch_date = body.get('launch_date')
            new_running_time = body.get('running_time')
            categories = body.get('categories')

            movie = Movie.query.filter_by(id=movie_id).first()

            convert_base64_to_image(new_banner_img_base64, movie.banner_img_id, IMG_PATH)
            convert_base64_to_image(new_poster_img_base64, movie.poster_img_id, IMG_PATH)

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
            movie.banner_img_id = movie.banner_img_id
            movie.poster_img_id = movie.poster_img_id
            movie.launch_date = new_launch_date
            movie.running_time = new_running_time

            db.session.commit()

            try:
                MovieCategory.query.filter_by(movie_id=movie.id).delete()
                db.session.commit()
                #print("Registros deletados com sucesso!")
            except Exception as e:
                db.session.rollback()
                print(f"Erro ao deletar registros: {e}")

            for category in categories:
                movie_category = MovieCategory(movie_id=movie.id, category_id=category)
                db.session.add(movie_category)

            db.session.commit()
            db.session.close()

            return jsonify({
                'status': 'ok',
                'message': 'Categoria modificada com sucesso'
            }),200
        
        except Exception as error:
                print_error_details(error)
                return jsonify({
                    'status': 'error',
                    'message': 'An error has occurred!',
                    'error_class': str(error.__class__),
                    'error_cause': str(error.__cause__)
                }),500
        
                
@movie_route.route('/api/v1/like_movie', methods=['POST'])
def like_movie():
    if request.method == 'POST':
        try:
            body = request.get_json()
            user_id = body.get('user_id')
            movie_id = body.get('movie_id')
            
            liked = Liked(user_id=user_id, movie_id=movie_id)
            
            db.session.add(liked)
            db.session.commit()
            db.session.close()
            
            return jsonify({
                'status': 'ok',
                'message': 'filme curtido com sucesso!',
            }), 200
            
        except Exception as error:
                print_error_details(error)
                return jsonify({
                    'status': 'error',
                    'message': 'An error has occurred!',
                    'error_class': str(error.__class__),
                    'error_cause': str(error.__cause__)
                }),500
        

@movie_route.route('/api/v1/get_liked_movies', methods=['GET'])
def get_liked_movies():
    try:
        if request.method == 'GET':
            id = request.args.get('id')

            liked_movie = Liked.query.filter_by(user_id=id).all()
            liked_movie_schema = LikedSchema(many=True)
            payload = liked_movie_schema.dump(liked_movie)

            if payload is None:
                return jsonify({
                    'status': 'error',
                    'message': 'Nenhum dado encontrado!'
                }), 404
            
            for i, _ in enumerate(payload):
                category = MovieCategory.query.filter_by(movie_id=payload[i]['movie']['id'])
                category_schema = MovieCategorySchema(many=True)
                payCat = category_schema.dump(category)

                print(payload[i]['movie']['title'])
                print(payload[i]['movie']['id'])
                print(payCat[i]['category'])
                

            for i, _ in enumerate(payload):
                payload[i]['movie']['banner_img'] = convert_image_to_base64(IMG_PATH, payload[i]['movie']['banner_img_id'])
                payload[i]['movie']['poster_img'] = convert_image_to_base64(IMG_PATH, payload[i]['movie']['poster_img_id'])

            return jsonify({
                'status': 'ok',
                'message': 'filme encontrados com sucesso!',
                'liked_movie': payload
            }), 200
    
    except Exception as error:
                print_error_details(error)
                return jsonify({
                    'status': 'error',
                    'message': 'An error has occurred!',
                    'error_class': str(error.__class__),
                    'error_cause': str(error.__cause__)
                }),500