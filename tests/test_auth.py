from http import HTTPStatus

from fast_api.models import User


def test_get_token(client, user: User):
    response = client.post(
        '/auth/token',
        data={'username': user.email, 'password': user.clean_password},
    )

    token = response.json()
    assert response.status_code == HTTPStatus.OK
    assert token['token_type'] == 'Bearer'
    assert 'access_token' in token


def test_get_token_fail(client, user: User):
    response = client.post(
        '/auth/token',
        data={'username': user.username, 'password': user.clean_password},
    )

    token = response.json()
    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert 'token_type' not in token
    assert 'access_token' not in token
