from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from fast_api_zero.models import User


class UserRepository:
    def __init__(self, session: Session):
        self.session = session

    def get_user_by_id(self, user_id: int) -> User:
        stmt = self.session.scalar(select(User).where(User.id == user_id))
        return stmt

    def get_user_by_username(self, username: str) -> User:
        stmt = self.session.scalar(
            select(User).where(User.username == username)
        )
        return stmt

    def get_all_users(self) -> list[User]:
        stmt = self.session.scalars(select(User)).all()
        return stmt

    def create_user(self, username: str, email: str, password: str) -> User:
        new_user = User(username=username, email=email, password=password)
        try:
            self.session.add(new_user)
            self.session.commit()
            self.session.refresh(new_user)
        except IntegrityError:
            self.session.rollback()
            raise ValueError('Failed to create user')
        return new_user

    def delete_user(self, user_id: int) -> bool:
        user = self.get_user_by_id(user_id)
        if user:
            self.session.delete(user)
            self.session.commit()
            return True
        return False

    def update_user(
        self,
        user_id: int,
        username: str = None,
        email: str = None,
        password: str = None,
    ) -> User:
        db_user = self.session.scalar(select(User).where(User.id == user_id))
        if not db_user:
            raise ValueError('User not found')

        update_data = {
            'username': username,
            'email': email,
            'password': password,
        }

        for key, value in update_data.items():
            if value is not None:
                setattr(db_user, key, value)
        self.session.add(db_user)
        self.session.commit()
        self.session.refresh(db_user)
        return db_user
