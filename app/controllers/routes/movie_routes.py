from flask import jsonify, request, Blueprint
from app.models.tables.movie import Movie
from app.models.tables.liked import Liked
from app.controllers.utils.functions import print_error_details
from app.models.schemas.movie_schema import MovieSchema
from app.extensions import db


movie_route = Blueprint('movie_route', __name__)

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
            movies = Movie.query.all()
            movies_schema = MovieSchema(many=True)
            payload = movies_schema.dump(movies)

            return jsonify({
                'movies': payload
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