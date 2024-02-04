from helpers import *

def test_add_category():
    payload = {
        'name': 'test_category'
    }

    create_category_response = create_category(payload)
    assert create_category_response.status_code == 201

    get_one_category_response = get_one_category(name=payload.get('name'))
    assert get_one_category_response.status_code == 200
    
    
    body = get_one_category_response.json()
    category_id = body.get('category').get('id')

    delete_category_payload = {
        'id': category_id
    }

    delete_category_response = delete_category(delete_category_payload)
    assert delete_category_response.status_code == 200

    get_add_category_response = get_one_category(category_id)
    assert get_add_category_response.status_code == 404
    
    
def test_delete_category():
    payload = {
        'name': 'test_category'
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
        'name': 'test_category'
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
        'name': 'test_category'
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
    
    