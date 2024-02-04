from helpers import *


def test_get_movies():
    
    create_category_payload = {
        'name': 'test_category'
    }
    
    create_category_response = create_category(payload=create_category_payload)
    assert create_category_response.status_code == 201
    
    get_one_category_response = get_one_category(name=create_category_payload.get('name'))
    assert get_one_category_response.status_code == 200
    
    category_reponse_body = get_one_category_response.json()
    assert category_reponse_body.get('category').get('name') == create_category_payload.get('name')
    
    payload = {
        "title": "title test",
        "original_title": "original title test",
        "romanized_original_title": "romanized title test",
        "description": "description test",
        "studio": "studio test",
        "director": "director test",
        "producer": "producer test",
        "rating": 10,
        "banner_img_id": "banner img id test",
        "poster_img_id": "poster img id test",
        "launch_date": "1999",
        "running_time": 102,
        "category_id": category_reponse_body.get('category').get('id')
    }

    add_movie_reponse = add_movie(payload=payload)
    assert add_movie_reponse.status_code == 201

    get_one_movie_reponse = get_one_movie(payload.get('title'), payload.get('studio'))
    assert get_one_movie_reponse.status_code == 200
    movie = get_one_movie_reponse.json()
    assert movie.get('movie').get('title') == payload.get('title')
    assert movie.get('movie').get('studio') == payload.get('studio')
    
    delete = {
        'id': movie.get('movie').get('id')
    }

    delete_movie_response = delete_movie(delete)
    assert delete_movie_response.status_code == 200

    get_one_movie_reponse = get_one_movie(payload.get('title'), payload.get('studio'))
    assert get_one_movie_reponse.status_code == 404
    
    delete_category_payload = {
        "id": category_reponse_body.get('category').get('id')
    }
    
    detele_category_reponse = delete_category(payload=delete_category_payload)
    assert detele_category_reponse.status_code == 200


def test_edit_movie():
    category_payload = {
        'name': 'test_category'
    }

    create_category_response = create_category(category_payload)
    assert create_category_response.status_code == 201
    get_one_category_response = get_one_category(category_payload.get('name'))
    assert get_one_category_response.status_code == 200
    body = get_one_category_response.json()
    assert body.get('category').get('name') == category_payload.get('name')

    movie_payload = {
        "title": "title test",
        "original_title": "original title test",
        "romanized_original_title": "romanized title test",
        "description": "description test",
        "studio": "studio test",
        "director": "director test",
        "producer": "producer test",
        "rating": 10,
        "banner_img_id": "banner img id test",
        "poster_img_id": "poster img id test",
        "launch_date": "1999",
        "running_time": 102,
        "category_id": body.get('category').get('id')
    }

    add_movie_response = add_movie(movie_payload)
    assert add_movie_response.status_code == 201

    get_one_movie_response = get_one_movie(movie_payload.get('title'), movie_payload.get('studio'))
    assert get_one_movie_response.status_code == 200
    movie_body = get_one_movie_response.json()
    assert movie_body.get('movie').get('title') == movie_payload.get('title')
    assert movie_body.get('movie').get('studio') == movie_payload.get('studio')

    id = movie_body.get('movie').get('id')

    movie_edit_payload = {
        "id": id,
        "title": "title test2",
        "original_title": "original title test2",
        "romanised_original_title": "romanised title test2",
        "description": "description test2",
        "studio": "studio test2",
        "director": "director test2",
        "producer": "producer test2",
        "rating": 10,
        "banner_img_id": "banner img id test2",
        "poster_img_id": "poster img id test2",
        "launch_date": "1992",
        "running_time": 102,
        "category_id": body.get('category').get('id')
    }

    edit_movie_response = edit_movie(movie_edit_payload)
    assert edit_movie_response.status_code == 200

    get_one_movie_response = get_one_movie(movie_edit_payload.get('title'), movie_edit_payload.get('studio'))
    assert get_one_movie_response.status_code == 200

    movie = get_one_movie_response.json()
    assert movie.get('movie').get('title') == movie_edit_payload.get('title')
    assert movie.get('movie').get('studio') == movie_edit_payload.get('studio')

    delete_movie_ = {
        'id': movie.get('movie').get('id')
    }

    delete_movie_response = delete_movie(delete_movie_)
    assert delete_movie_response.status_code == 200

    get_one_movie_response = get_one_movie(movie_edit_payload.get('title'), movie_edit_payload.get('studio'))
    assert get_one_movie_response.status_code == 404

    id = body.get('category').get('id')
       

    delete_category_ = {
        'id': id
    }

    delete_category_response = delete_category(delete_category_)
    assert delete_category_response.status_code == 200

    get_one_category_response = get_one_category(delete_category_.get('id'))
    assert get_one_category_response.status_code == 404
