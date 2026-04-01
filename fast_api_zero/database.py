from fastapi import Depends
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from fast_api_zero.settings import Settings
from fast_api_zero.user_repository import UserRepository

engine = create_engine(Settings().DATABASE_URL)


def get_session():
    with Session(engine) as session:
        yield session


def get_user_repository(session: Session = Depends(get_session)):
    return UserRepository(session)
