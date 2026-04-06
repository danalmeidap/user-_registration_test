from contextlib import contextmanager
from datetime import datetime

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import StaticPool, create_engine, event
from sqlalchemy.orm import Session

from fast_api_zero.app import app
from fast_api_zero.database import get_session
from fast_api_zero.models import User, table_registry
from fast_api_zero.security import get_password_hash


@pytest.fixture
def client(session):
    def get_session_override():
        return session

    app.dependency_overrides[get_session] = get_session_override
    with TestClient(app) as client:
        yield client
    app.dependency_overrides.clear()


@pytest.fixture
def session():
    engine = create_engine(
        'sqlite:///:memory:',
        connect_args={'check_same_thread': False},
        poolclass=StaticPool,
    )
    table_registry.metadata.create_all(engine)

    with Session(engine) as session:
        yield session

    table_registry.metadata.drop_all(engine)
    engine.dispose()


@pytest.fixture
def mock_db_time():
    return _mock_db_time


@contextmanager
def _mock_db_time(*, model, time=datetime(2024, 1, 1)):
    def fake_time_handler(mapper, connection, target):
        if hasattr(target, 'created_at'):
            target.created_at = time
        if hasattr(target, 'updated_at'):
            target.updated_at = time

    event.listen(model, 'before_insert', fake_time_handler)
    try:
        yield time
    finally:
        event.remove(model, 'before_insert', fake_time_handler)


@pytest.fixture
def token(client: TestClient, session: Session):
    password = 'test_password'
    user = User(
        username='test_user_fixture',
        email='fixture@example.com',
        password=get_password_hash(password),
    )
    session.add(user)
    session.commit()
    session.refresh(user)
    response = client.post(
        '/token', data={'username': user.username, 'password': password}
    )
    return response.json()['access_token']
