from fastapi import status
from fastapi.testclient import TestClient

from fast_api_zero.token import create_access_token


def test_get_current_user_no_username_payload(client):
    bad_token = create_access_token(data={})
    response = client.get(
        '/users/all', headers={'Authorization': f'Bearer {bad_token}'}
    )
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.json()['detail'] == 'Could not validate credentials'


def test_get_current_user_decode_error(client):
    bad_token = 'token_que_nao_segue_o_padrao_jwt'
    response = client.get(
        '/users/all', headers={'Authorization': f'Bearer {bad_token}'}
    )
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_get_current_user_not_found_in_db(client):
    token_ghost = create_access_token(data={'sub': 'usuario_fantasma'})
    response = client.get(
        '/users/all', headers={'Authorization': f'Bearer {token_ghost}'}
    )
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.json()['detail'] == 'Could not validate credentials'


def test_login_should_success(client: TestClient):
    client.post(
        '/users/',
        json={
            'username': 'testuser',
            'email': 'test@example.com',
            'password': 'password123',
        },
    )

    login_data = {'username': 'testuser', 'password': 'password123'}
    response = client.post('/token', data=login_data)

    token_data = response.json()
    assert 'access_token' in token_data
    assert response.status_code == status.HTTP_200_OK
    assert token_data['token_type'] == 'bearer'


def test_login_user_not_found(client: TestClient):
    login_data = {
        'username': 'usuario_inexistente',
        'password': 'qualquer_password',
    }
    response = client.post('/token', data=login_data)

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json()['detail'] == 'User not found'


def test_login_wrong_password(client: TestClient):
    client.post(
        '/users/',
        json={
            'username': 'daniel',
            'email': 'daniel@teste.com',
            'password': 'password_correta',
        },
    )

    login_data = {'username': 'daniel', 'password': 'password_errada'}
    response = client.post('/token', data=login_data)

    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.json()['detail'] == 'Invalid credentials'
    assert response.headers['WWW-Authenticate'] == 'bearer'
