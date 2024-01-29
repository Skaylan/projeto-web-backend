import requests
from requests import Response
import jwt
import os

ENDPOINT = 'http://localhost:5000/api/v1'
SECRET_KEY = os.getenv('SECRET_KEY')

def test_create_user():
    payload = {
        'name': 'test_name',
        'username': 'test_username',
        'email': 'test_email@email.com',
        'password': 'testpassword',
        're_password': 'testpassword',
    }
    
    create_user_response = create_user(payload)
    status = create_user_response.status_code
    assert status == 201
    
    delete_user_payload = {
        'username': payload.get('username'),
        'password': payload.get('password')
    }
    
    delete_user_response = delete_user(delete_user_payload)
    assert delete_user_response.status_code == 200


def test_delete_user():
    payload = {
        'name': 'test_name',
        'username': 'test_username',
        'email': 'test_email@email.com',
        'password': 'testpassword',
        're_password': 'testpassword',
    }
    
    create_user_response = create_user(payload)
    assert create_user_response.status_code == 201
    
    delete_payload = {
        'username': payload.get('username'),
        'password': payload.get('password')
    }
    
    delete_user_response = delete_user(delete_payload)
    assert delete_user_response.status_code == 200
    
    get_user_response = get_one_user(payload.get('email'))
    assert get_user_response.status_code == 404


def test_get_users():
    get_many_users_response = get_many_users()
    assert get_many_users_response.status_code == 200
    users_object = get_many_users_response.json()
    assert str(type(users_object)) == "<class 'dict'>"

def test_get_one_user():
    payload = {
        'name': 'test_name',
        'username': 'test_username',
        'email': 'test_email@email.com',
        'password': 'testpassword',
        're_password': 'testpassword',
    }
    
    create_user_response = create_user(payload=payload)
    assert create_user_response.status_code == 201
    
    get_one_user_response = get_one_user(email=payload.get('email'))
    assert get_one_user_response.status_code == 200
    user_data = get_one_user_response.json()
    assert user_data.get('user').get('email') == payload.get('email')
    
    delete_user_payload = {
        'username': payload.get('username'),
        'password': payload.get('password')
    }
    delete_user_response = delete_user(payload=delete_user_payload)
    assert delete_user_response.status_code == 200


def test_delete_category():
    payload = {
        'name': 'testename'
    }

    create_category_response = create_category(payload)
    assert create_category_response.status_code == 201
    
    get_one_category_response = get_one_category(payload.get('name'))
    assert get_one_category_response.status_code == 200
    body = get_one_category_response.json()
    assert body.get('category').get('name') == payload.get('name')

    id = body.get('category').get('id')
    delete_payload = {
        'id': id
    } 
    delete_category_response = delete_category(delete_payload)
    assert delete_category_response.status_code == 200
    
    get_one_category_response = get_one_category(payload.get('name'))
    assert get_one_category_response.status_code == 404


def test_get_categories():
    payload = {
        'name': 'testecategory'
    }

    create_category_response = create_category(payload)
    assert create_category_response.status_code == 201

    get_category_response = get_categories()
    assert get_category_response.status_code == 200
    body = get_category_response.json()
    assert str(type(body)) == "<class 'dict'>"

    id = body.get('categories')[-1].get('id')

    delete = {
        'id': id
    }

    delete_category_response = delete_category(delete)
    assert delete_category_response.status_code == 200


def test_edit_category():
    payload = {
        'name': 'testecategory'
    }

    create_category_response = create_category(payload)
    assert create_category_response.status_code == 201

    get_one_category_response = get_one_category(payload.get('name'))
    assert get_one_category_response.status_code == 200

    body = get_one_category_response.json()
    assert body.get('category').get('name') == payload.get('name')

    category_edit = {
        'new_name': 'testecategory2',
        'category_id': body.get('category').get('id')
    }

    edit_category_response = edit_category(category_edit)
    assert edit_category_response.status_code == 200

    get_one_category_response = get_one_category(category_edit.get('new_name'))
    assert get_one_category_response.status_code == 200

    body = get_one_category_response.json()
    assert body.get('category').get('name') == category_edit.get('new_name')

    delete = {
        'id': body.get('category').get('id')
    }

    delete_category_response = delete_category(delete)
    assert delete_category_response.status_code == 200
    
    
def test_authenticate():
    payload = {
        'name': 'test_name',
        'username': 'test_username',
        'email': 'test_email@email.com',
        'password': 'testpassword',
        're_password': 'testpassword',
    }
    
    create_response = create_user(payload=payload)
    assert create_response.status_code == 201
    
    auth_payload = {
        'email': payload.get('email'),
        'password': payload.get('password')
    }
    
    authenticate_reponse = authenticate(payload=auth_payload)
    assert authenticate_reponse.status_code == 200
    
    delete_payload = {
        'username': payload.get('username'),
        'password': payload.get('password')
    }
    
    delete_user_response = delete_user(payload=delete_payload)
    assert delete_user_response.status_code == 200
    
    get_user_response = get_one_user(email=payload.get('email'))
    assert get_user_response.status_code == 404
    get_user_body = get_user_response.json()
    assert get_user_body.get('user') == None


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


def create_user(payload: dict) -> Response: 
    return requests.post(ENDPOINT + '/create_user', json=payload)

def delete_user(payload: dict) -> Response:
    return requests.delete(ENDPOINT + '/delete_user', json=payload)

def get_one_user(email: str) -> Response:
    return requests.get(ENDPOINT + '/get_one_user', params={'email': email})

def get_many_users() -> Response:
    return requests.get(ENDPOINT + '/get_users')

def create_category(payload: dict) -> Response:
    return requests.post(ENDPOINT + '/add_category', json=payload)

def delete_category(payload: dict) -> Response:
    return requests.delete(ENDPOINT + '/delete_category', json=payload)

def get_categories() -> Response:
    return requests.get(ENDPOINT + '/get_categories')

def get_one_category(name: str) -> Response:
    return requests.get(ENDPOINT + '/get_one_category', params={'name': name})

def edit_category(payload: dict) -> Response:
    return requests.put(ENDPOINT + '/edit_category', json=payload)

def authenticate(payload: dict) -> Response:
    return requests.post(ENDPOINT + '/authenticate', json=payload)

def add_movie(payload:dict) -> Response:
    return requests.post(ENDPOINT + '/add_movie', json=payload)

def get_movies() -> Response:
    return requests.get(ENDPOINT + '/get_movies')

def get_one_movie(title: str, studio: str) -> Response:
    return requests.get(ENDPOINT + '/get_one_movie', params={'title': title, 'studio': studio})

def delete_movie(payload: dict) -> Response:
    return requests.delete(ENDPOINT + '/delete_movie', json=payload)