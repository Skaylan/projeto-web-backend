from helpers import *


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
    
    
    auth_user_body = authenticate_reponse.json()
    auth_token = auth_user_body.get('token')
    logout_user_response = logout({'token': auth_token})
    assert logout_user_response.status_code == 200
    
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