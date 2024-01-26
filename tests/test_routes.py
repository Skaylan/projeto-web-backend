import requests
from requests import Response

ENDPOINT = 'http://localhost:5000/api/v1'


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
    
    get_user_response = get_one_user(payload.get('username'))
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
    
    get_one_user_response = get_one_user(username=payload.get('username'))
    assert get_one_user_response.status_code == 200
    user_data = get_one_user_response.json()
    assert user_data.get('user').get('username') == payload.get('username')
    
    delete_user_payload = {
        'username': payload.get('username'),
        'password': payload.get('password')
    }
    delete_user_response = delete_user(payload=delete_user_payload)
    assert delete_user_response.status_code == 200
    


def create_user(payload: dict) -> Response:
    return requests.post(ENDPOINT + '/create_user', json=payload)

def delete_user(payload: dict) -> Response:
    return requests.delete(ENDPOINT + '/delete_user', json=payload)

def get_one_user(username: str) -> Response:
    return requests.get(ENDPOINT + '/get_one_user', params={'username': username})

def get_many_users() -> Response:
    return requests.get(ENDPOINT + '/get_users')