import requests
import os
from requests import Response

ENDPOINT = 'http://localhost:5000/api/v1'
SECRET_KEY = os.getenv('SECRET_KEY')

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

def edit_movie(payload: dict) -> Response:
    return requests.put(ENDPOINT + '/edit_movie', json=payload)