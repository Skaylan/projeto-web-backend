from helpers import *

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
