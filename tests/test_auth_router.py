from fastapi import status
from fastapi.testclient import TestClient


def test_login_should_success(client: TestClient):
    client.post("/users/", json={
        "username": "testuser",
        "email": "test@example.com",
        "password": "password123"
    })

    login_data = {
        "username": "testuser",
        "password": "password123"
    }
    response = client.post('/auth/login', data=login_data)

    assert response.status_code == status.HTTP_200_OK


def test_login_should_fail_invalid_credentials(client: TestClient):
    client.post("/users/", json={
        "username": "testuser",
        "email": "test@example.com",
        "password": "password123"
    })

    login_data = {
        "username": "testuser",
        "password": "wrongpassword"
    }
    response = client.post('/auth/login', data=login_data)

    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.json() == {
        "detail": "Invalid credentials"}


def test_login_should_fail_user_not_found(client: TestClient):
    login_data = {
        "username": "nonexistentuser",
        "password": "password123"
    }
    response = client.post('/auth/login', data=login_data)

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {
        "detail": "User not found"}
