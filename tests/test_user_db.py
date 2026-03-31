from contextlib import _GeneratorContextManager
from dataclasses import asdict
from datetime import datetime, timezone

import pytest
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from fast_api_zero.models import User
from fast_api_zero.user_repository import UserRepository


def test_create_user_db(
    session: Session,
    mock_db_time: _GeneratorContextManager[datetime, None, None],
):
    with mock_db_time(model=User) as time:
        new_user = User(
            username='alice', password='secret', email='teste@test'
        )
        session.add(new_user)
        session.commit()

    user = session.scalar(select(User).where(User.username == 'alice'))
    user_dict = asdict(user)

    assert user_dict['username'] == 'alice'
    assert user_dict['email'] == 'teste@test'
    assert user_dict['password'] == 'secret'

    assert isinstance(user_dict['created_at'], datetime)
    assert isinstance(user_dict['updated_at'], datetime)

    assert user_dict['created_at'] == time


def test_create_user_repository_integrity_error(session):
    data = {'username': 'dan', 'email': 'dan@aracaju.com', 'password': '123'}
    repo = UserRepository(session)
    repo.create_user(**data)
    with pytest.raises(ValueError, match='Failed to create user'):
        repo.create_user(**data)


def test_create_user_duplicate_user(session: Session):
    user = User(username='bob', password='secret', email='bob@test')
    session.add(user)
    session.commit()
    duplicate_user = User(username='bob', password='secret', email='bob@test')
    session.add(duplicate_user)
    with pytest.raises(IntegrityError):
        session.commit()


def test_create_user_invalid_data(session: Session):
    invalid_user = User(username=None, password='secret', email='invalid@test')
    session.add(invalid_user)
    with pytest.raises(IntegrityError):
        session.commit()


def create_user_duplicate_email(session: Session):
    user1 = User(username='user1', password='secret', email='duplicate@test')
    user2 = User(username='user2', password='secret', email='duplicate@test')
    session.add(user1)
    session.add(user2)
    with pytest.raises(IntegrityError):
        session.commit()


def test_get_user_by_id_db(session: Session):
    user = User(username='bob', password='secret', email='bob@test')
    session.add(user)
    session.commit()
    user = session.scalar(select(User).where(User.id == 1))
    assert user.id == 1


def test_get_user_by_id_not_found_db(session: Session):
    fake_indice = 999
    user = session.scalar(select(User).where(User.id == fake_indice))
    assert user is None


def test_get_user_by_username_db(session: Session):
    user = User(username='charlie', password='secret', email='charlie@test')
    session.add(user)
    session.commit()
    user = session.scalar(select(User).where(User.username == 'charlie'))
    assert user.username == 'charlie'


def test_get_user_by_username_not_found_db(session: Session):
    user = session.scalar(select(User).where(User.username == 'nonexistent'))
    assert user is None


def test_get_user_by_email_db(session: Session):
    user = User(username='dave', password='secret', email='dave@test')
    session.add(user)
    session.commit()
    user = session.scalar(select(User).where(User.email == 'dave@test'))
    assert user.email == 'dave@test'


def test_get_user_by_email_not_found_db(session: Session):
    user = session.scalar(select(User).where(User.email == 'nonexistent@test'))
    assert user is None


def test_get_all_users_db(session: Session):
    correct_len = 2
    users = [
        User(username='eve', password='secret', email='eve@test'),
        User(username='frank', password='secret', email='frank@test'),
    ]
    session.add_all(users)
    session.commit()
    users = session.scalars(select(User)).all()
    assert len(users) == correct_len
    assert users[0].username == 'eve'
    assert users[1].username == 'frank'


def test_get_all_users_empty_db(session: Session):
    users = session.scalars(select(User)).all()
    assert len(users) == 0


def test_delete_user_db(session: Session):
    user = User(username='grace', password='secret', email='grace@test')
    session.add(user)
    session.commit()
    session.delete(user)
    session.commit()
    user = session.scalar(select(User).where(User.username == 'grace'))
    assert user is None


def test_delete_user_not_found_db(session: Session):
    fake_indice = 999
    user = session.scalar(select(User).where(User.id == fake_indice))
    assert user is None


def test_update_user_db(
    session: Session,
    mock_db_time: _GeneratorContextManager[datetime, None, None],
):
    with mock_db_time(model=User):
        new_user = User(
            username='alice', password='secret', email='teste@test'
        )
        session.add(new_user)
        session.commit()
    user = session.scalar(select(User).where(User.username == 'alice'))
    user.password = 'new_secret'
    session.commit()
    now = datetime.now(timezone.utc).replace(tzinfo=None)
    assert user.updated_at <= now
    assert user.password == 'new_secret'


def test_update_user_not_found_db(session: Session):
    fake_indice = 999
    user = session.scalar(select(User).where(User.id == fake_indice))
    assert user is None


def test_update_user_not_found(session):
    repo = UserRepository(session)
    with pytest.raises(ValueError, match='User not found'):
        repo.update_user(user_id=999, username='new_name')
