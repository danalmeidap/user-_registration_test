from fastapi import status
from fastapi.testclient import TestClient


def test_login_success(client: TestClient):
    client.post("/users/", json={
        "username": "testuser",
        "email": "test@example.com",
        "password": "password123"
    })
    login_data = {
        "email": "test@example.com",
        "password": "password123"
    }
    response = client.post('/auth/login', json=login_data)
    assert response.status_code == status.HTTP_200_OK


def test_login_invalid_credentials(client: TestClient):
    client.post("/users/", json={
        "username": "testuser",
        "email": "test@example.com",
        "password": "password123"
    })

    login_data = {
        "email": "test@example.com",
        "password": "wrongpassword"
    }

    response = client.post('/auth/login', json=login_data)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.json()["detail"] == 'Invalid credentials'
