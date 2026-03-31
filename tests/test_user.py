from contextlib import _GeneratorContextManager
from datetime import datetime, timedelta

from fastapi import status
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from fast_api_zero.models import User
from fast_api_zero.user_repository import UserRepository
from fast_api_zero.users import get_user_repository


def test_get_user_repository(session: Session):
    repository = get_user_repository(session)
    assert isinstance(repository, UserRepository)
    assert repository.session == session


def test_read_users_route_is_active(client: TestClient):
    response = client.get('/users/all')
    assert response.status_code == status.HTTP_200_OK


def test_create_user_and_check_mock_time(client: TestClient,
    mock_db_time: _GeneratorContextManager):
    frozen_time = datetime(2026, 1, 1, 12, 0, 0)
    with mock_db_time(model=User, time=frozen_time):
        payload = {
            "username": "time_traveler",
            "email": "past@future.com",
            "password": "password123"

        }
        response = client.post('/users/', json=payload)
        assert response.status_code == status.HTTP_201_CREATED

        data = response.json()
        assert data["created_at"] == frozen_time.isoformat()
        assert data["updated_at"] == frozen_time.isoformat()


def test_create_user_duplicate_error_full_flow(client):

    user_payload = {
        "username": "dan_tecladista",
        "email": "dan@aracaju.se.br",
        "password": "123"
    }
    response_1 = client.post("/users/", json=user_payload)
    assert response_1.status_code == status.HTTP_201_CREATED

    response_2 = client.post("/users/", json=user_payload)

    assert response_2.status_code == status.HTTP_400_BAD_REQUEST
    assert response_2.json()["detail"] == 'Failed to create user'


def test_get_user_by_id_not_found(client: TestClient):
    response = client.get('/users/999/')
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json()["detail"] == "User not found"


def test_get_user_by_id_success(client: TestClient):
    payload = {
        "username": "testuser",
        "email": "testuser@example.com",
        "password": "password123"
    }
    response = client.post('/users/', json=payload)
    user_id = response.json()["id"]

    response = client.get(f'/users/{user_id}/')
    assert response.status_code == status.HTTP_200_OK


def test_get_all_users_returns_list(client: TestClient):
    response = client.get('/users/all')
    assert response.status_code == status.HTTP_200_OK
    assert isinstance(response.json(), list)


def test_delete_user_not_found(client: TestClient):
    response = client.delete('/users/999/')
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json()["detail"] == "User not found"


def test_delete_user_success(client: TestClient):
    payload = {
        "username": "tobedeleted",
        "email": "tobedeleted@example.com",
        "password": "secretpassword"
    }
    response = client.post('/users/', json=payload)
    user_id = response.json()["id"]

    response = client.delete(f'/users/{user_id}/')
    assert response.status_code == status.HTTP_204_NO_CONTENT
    response = client.get(f'/users/{user_id}/')
    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_update_user_and_check_mock_time(client, mock_db_time):
    t1 = datetime(2026, 1, 1, 12, 0, 0)
    t2 = t1 + timedelta(hours=3)
    with mock_db_time(model=User, time=t1):
        create_payload = {
            "username": "jose_tecladista",
            "email": "jose@musica.com",
            "password": "senha_segura"
        }
        resp_create = client.post('/users/', json=create_payload)
        assert resp_create.status_code == status.HTTP_201_CREATED
        user_id = resp_create.json()["id"]

    with mock_db_time(model=User, time=t2):
        update_payload = {
            "username": "jose_backend",
            "email": "jose@dev.com",
            "password": "nova_senha_123"
        }
        response = client.put(f'/users/{user_id}', json=update_payload)
        assert response.status_code == status.HTTP_200_OK

        json_res = response.json()
        assert json_res["username"] == "jose_backend"
        assert json_res["email"] == "jose@dev.com"


def test_update_user_not_found_returns_404(client):
    user_id_inexistente = 999
    payload = {
        "username": "qualquer_nome",
        "email": "teste@teste.com",
        "password": "123"
    }

    response = client.put(f'/users/{user_id_inexistente}', json=payload)

    # 3. Asserts
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json()['detail'] == 'User not found'
