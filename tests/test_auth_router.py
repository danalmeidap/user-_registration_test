from fastapi import status
from fastapi.testclient import TestClient


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
    response = client.post('/auth/login', data=login_data)

    token_data = response.json()
    assert 'access_token' in token_data
    assert response.status_code == status.HTTP_200_OK
    assert token_data['token_type'] == 'bearer'


def test_login_user_not_found(client: TestClient):
    login_data = {
        'username': 'usuario_inexistente',
        'password': 'qualquer_password',
    }
    response = client.post('/auth/login', data=login_data)

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
    response = client.post('/auth/login', data=login_data)

    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.json()['detail'] == 'Invalid credentials'
    assert response.headers['WWW-Authenticate'] == 'bearer'
