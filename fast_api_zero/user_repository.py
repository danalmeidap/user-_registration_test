from sqlalchemy import select
from sqlalchemy.orm import Session

from fast_api_zero.models import User


class UserRepository:
    def __init__(self, session: Session):
        self.session = session

    def get_user_by_id(self, user_id: int) -> User:
        stmt = self.session.scalar(select(User).where(User.id == user_id))
        return stmt

    def get_all_users(self) -> list[User]:
        stmt = self.session.scalars(select(User)).all()
        return stmt

    def create_user(self, username: str, email: str, password: str) -> User:
        if self.verify_user(email, username, password):
            raise ValueError('User already exists')
        new_user = User(username=username, email=email, password=password)
        self.session.add(new_user)
        self.session.commit()
        self.session.refresh(new_user)
        return new_user

    def verify_user(self, email: str, username: str, password: str) -> User:
        stmt = self.session.scalar(select(User).where(User.email == email))
        return (stmt and stmt.username == username
        and stmt.password == password
        and stmt.email == email)

    def delete_user(self, user_id: int) -> bool:
        user = self.get_user_by_id(user_id)
        if user:
            self.session.delete(user)
            self.session.commit()
            return True
        return False

    def update_user(self, user_id: int,
                    username: str = None,
                    email: str = None,
                    password: str = None) -> User:
        user = self.get_user_by_id(user_id)
        if not user:
            return None
        if username:
            user.username = username
        if email:
            user.email = email
        if password:
            user.password = password
        self.session.commit()
        self.session.refresh(user)
        return user
