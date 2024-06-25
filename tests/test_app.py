from http import HTTPStatus


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


def test_get_by_user_id(client):
    response = client.get('/users/1')
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'id': 1,
        'username': 'string',
        'email': 'user@example.com',
    }
    response = client.get('/users/2')
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'User not found'}


def test_read_user(client):
    response = client.get('/users/')

    assert response.status_code == HTTPStatus.OK

    assert response.json() == {
        'users': [
            {
                'id': 1,
                'username': 'string',
                'email': 'user@example.com',
            }
        ]
    }


def test_update_user(client):
    response = client.put(
        '/users/1',
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

    response = client.put(
        '/users/2',
        json={
            'id': 1,
            'username': 'test_update_user',
            'email': 'user@example.com',
            'password': 'string',
        },
    )

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'User not found'}


def test_delete_user(client):
    response = client.delete('/users/1')
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'User deleted!'}
    response = client.delete('/users/2')
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'User not found'}
