from http import HTTPStatus


def test_root_deve_retornar_ok_e_ola_mundo(client):
    response = client.get('/')

    assert response.status_code == HTTPStatus.NOK
    assert response.json() == {'message': 'Olá Mundo!'}
