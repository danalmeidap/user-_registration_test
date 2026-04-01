from contextlib import _GeneratorContextManager
from datetime import datetime

from fastapi import status
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from fast_api_zero.deps import get_current_user
from fast_api_zero.models import User
from fast_api_zero.user_repository import UserRepository
from fast_api_zero.users import get_user_repository


def test_get_user_repository(session: Session):
    repository = get_user_repository(session)
    assert isinstance(repository, UserRepository)
    assert repository.session == session


def test_read_users_route_is_active(client, token):
    response = client.get(
        '/users/all',
        headers={'Authorization': f'Bearer {token}'}
    )
    assert response.status_code == status.HTTP_200_OK


def test_create_user_and_check_mock_time(
    client: TestClient, mock_db_time: _GeneratorContextManager
):
    frozen_time = datetime(2026, 1, 1, 12, 0, 0)
    with mock_db_time(model=User, time=frozen_time):
        payload = {
            'username': 'time_traveler',
            'email': 'past@future.com',
            'password': 'password123',
        }
        response = client.post('/users/', json=payload)
        assert response.status_code == status.HTTP_201_CREATED

        data = response.json()
        assert data['created_at'] == frozen_time.isoformat()
        assert data['updated_at'] == frozen_time.isoformat()


def test_create_user_duplicate_error_full_flow(client):
    user_payload = {
        'username': 'dan_tecladista',
        'email': 'dan@aracaju.se.br',
        'password': '123',
    }
    response_1 = client.post('/users/', json=user_payload)
    assert response_1.status_code == status.HTTP_201_CREATED

    response_2 = client.post('/users/', json=user_payload)

    assert response_2.status_code == status.HTTP_400_BAD_REQUEST
    assert response_2.json()['detail'] == 'Failed to create user'


def test_get_user_by_id_not_found(client: TestClient):
    response = client.get('/users/999/')
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json()['detail'] == 'User not found'


def test_get_user_by_id_success(client: TestClient):
    payload = {
        'username': 'testuser',
        'email': 'testuser@example.com',
        'password': 'password123',
    }
    response = client.post('/users/', json=payload)
    user_id = response.json()['id']

    response = client.get(f'/users/{user_id}/')
    assert response.status_code == status.HTTP_200_OK


def test_get_all_users_returns_list(client: TestClient, token: str):
    response = client.get('/users/all',
     headers={'Authorization': f'Bearer {token}'})
    assert response.status_code == status.HTTP_200_OK
    assert isinstance(response.json(), list)


def test_delete_user_not_found(client: TestClient, token: str):
    response = client.delete('/users/999/',
            headers={'Authorization': f'Bearer {token}'})
    assert response.status_code == status.HTTP_403_FORBIDDEN
    assert response.json()['detail'] == 'Not authorized to delete this user'


def test_delete_user_success(client: TestClient):
    payload = {
        'username': 'tobedeleted',
        'email': 'tobedeleted@example.com',
        'password': 'secretpassword',
    }
    resp_create = client.post('/users/', json=payload)
    user_id = resp_create.json()['id']
    login_res = client.post(
        '/token',
        data={'username': 'tobedeleted', 'password': 'secretpassword'}
    )
    user_token = login_res.json()['access_token']
    response = client.delete(
        f'/users/{user_id}/',
        headers={'Authorization': f'Bearer {user_token}'}
    )

    assert response.status_code == status.HTTP_204_NO_CONTENT


def test_update_user_with_token(client: TestClient, token: str):
    update_payload = {
        'username': 'jose_backend',
        'email': 'jose@dev.com',
        'password': 'nova_senha_123'
    }
    response = client.put(
        '/users/1',
        json=update_payload,
        headers={'Authorization': f'Bearer {token}'}
    )
    assert response.status_code == status.HTTP_200_OK
    assert response.json()['username'] == 'jose_backend'


def test_update_user_not_found_returns_403(client: TestClient, token: str):
    user_id_inexistente = 999
    update_payload = {
        'username': 'jose_backend',
        'email': 'jose@dev.com',
        'password': 'nova_senha_123'
    }
    response = client.put(
        f'/users/{user_id_inexistente}',
        json=update_payload,
        headers={'Authorization': f'Bearer {token}'}
    )

    assert response.status_code == status.HTTP_403_FORBIDDEN
    assert response.json()['detail'] == 'Not authorized to update this user'


def test_repository_delete_user_not_found_directly(session):
    repo = UserRepository(session)
    result = repo.delete_user(user_id=999)
    assert result is False


def test_delete_user_not_found_forced(client, token):
    user_fake = User(username="admin", email="a@a.com", password="123")
    user_fake.id = 999

    def skip_user_check():
        return user_fake

    client.app.dependency_overrides[get_current_user] = skip_user_check

    response = client.delete(
        '/users/999/',
        headers={'Authorization': f'Bearer {token}'}
    )

    client.app.dependency_overrides.clear()
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json()['detail'] == 'User not found'


def test_update_user_not_found_forced(client, token):
    user_fake = User(username="admin", email="a@a.com", password="123")
    user_fake.id = 999

    def skip_user_check():
        return user_fake

    client.app.dependency_overrides[get_current_user] = skip_user_check
    payload = {
        'username': 'novo_nome',
        'email': 'novo@email.com',
        'password': 'nova_senha_123'
    }
    response = client.put(
        '/users/999',
        json=payload,
        headers={'Authorization': f'Bearer {token}'}
    )

    client.app.dependency_overrides.clear()

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert 'not found' in response.json()['detail'].lower()
