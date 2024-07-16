from http import HTTPStatus

from fast_api.models import User
from fast_api.schemas import UserPublic, UserSchema


def test_root_deve_retornar_ok_e_ola_mundo(client):
    response = client.get('/')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'Olá Mundo!'}


def test_create_user(client):
    response = client.post(
        '/users/',
        json={
            'username': 'string',
            'email': 'user@example.com',
            'password': 'string',
        },
    )

    assert response.status_code == HTTPStatus.CREATED
    assert response.json() == {
        'id': 1,
        'username': 'string',
        'email': 'user@example.com',
    }


def test_create_user_same_name(client, user: User):
    user_schema = UserSchema.model_validate(user).model_dump()
    response = client.post('/users/', json=user_schema)
    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json() == {'detail': 'Username already exists'}


def test_create_user_same_email(client, user: User):
    user_schema = UserSchema.model_validate(user).model_dump()
    user_schema['username'] = 'teste'
    response = client.post('/users/', json=user_schema)
    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json() == {'detail': 'Email already exists'}


def test_get_by_user_id(client, user: User):
    user_schema = UserPublic.model_validate(user).model_dump()
    response = client.get('/users/1')
    assert response.status_code == HTTPStatus.OK
    assert response.json() == user_schema
    response = client.get('/users/2')
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'User not found'}
    response = client.get('/users/-2')
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'User not found'}


def test_read_user(client):
    response = client.get('/users/')
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'users': []}


def test_read_user_with_user(client, user: User):
    user_schema = UserPublic.model_validate(user).model_dump()
    response = client.get('/users/')

    assert response.status_code == HTTPStatus.OK

    assert response.json() == {'users': [user_schema]}


def test_update_user(client, user: User, token):
    response = client.put(
        f'/users/{user.id}',
        headers={'Authorization': f'Bearer {token}'},
        json={
            'id': 1,
            'username': 'test_update_user',
            'email': 'user@example.com',
            'password': 'string',
        },
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'id': 1,
        'username': 'test_update_user',
        'email': 'user@example.com',
    }


def test_update_user_not_found(client, user: User, token):
    response = client.put(
        '/users/3',
        headers={'Authorization': f'Bearer {token}'},
        json={
            'id': 3,
            'username': 'test_update_user',
            'email': 'user@example.com',
            'password': 'string',
        },
    )
    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json() == {'detail': 'Not enough permission'}


def test_delete_user_with_user(client, user: User, token):
    response = client.delete(
        f'/users/{user.id}',
        headers={'Authorization': f'Bearer {token}'},
    )
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'User deleted!'}


def test_delete_user_without_user(client, user: User, token):
    response = client.delete(
        f'/users/{user.id + 1}',
        headers={'Authorization': f'Bearer {token}'},
    )
    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json() == {'detail': 'Not enough permission'}


def test_get_token(client, user: User):
    response = client.post(
        '/token',
        data={'username': user.email, 'password': user.clean_password},
    )

    token = response.json()
    assert response.status_code == HTTPStatus.OK
    assert token['token_type'] == 'Bearer'
    assert 'access_token' in token


def test_get_token_fail(client, user: User):
    response = client.post(
        '/token',
        data={'username': user.username, 'password': user.clean_password},
    )

    token = response.json()
    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert 'token_type' not in token
    assert 'access_token' not in token
