from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from fast_api_zero.database import get_session
from fast_api_zero.schemas import UserDB, UserSchema
from fast_api_zero.security import get_password_hash
from fast_api_zero.user_repository import UserRepository

user_router = APIRouter()


def get_user_repository(
    session: Session = Depends(get_session),
) -> UserRepository:
    return UserRepository(session)


@user_router.post(
    '/', status_code=status.HTTP_201_CREATED, response_model=UserDB
)
def create_user(
    user: UserSchema, repository: UserRepository = Depends(get_user_repository)
):
    try:
        new_user = repository.create_user(
            username=user.username,
            email=user.email,
            password=get_password_hash(user.password)
        )
        return UserDB(
            id=new_user.id,
            username=new_user.username,
            email=new_user.email,
            created_at=new_user.created_at,
            updated_at=new_user.updated_at,
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )


@user_router.get('/{user_id}/', response_model=UserDB)
def get_user_by_id(
    user_id: int, repository: UserRepository = Depends(get_user_repository)
):
    user = repository.get_user_by_id(user_id)
    if user:
        return UserDB(**user.__dict__)
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail='User not found',
    )


@user_router.get('/all', response_model=list[UserDB])
def get_all_users(repository: UserRepository = Depends(get_user_repository)):
    users = repository.get_all_users()
    return [UserDB(**user.__dict__) for user in users]


@user_router.delete('/{user_id}/', status_code=status.HTTP_204_NO_CONTENT)
def delete_user(
    user_id: int, repository: UserRepository = Depends(get_user_repository)
):
    success = repository.delete_user(user_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='User not found',
        )


@user_router.put('/{user_id}', response_model=UserDB)
def update_user(
    user_id: int,
    user: UserSchema,
    repository: UserRepository = Depends(get_user_repository),
):
    try:
        return repository.update_user(user_id=user_id,
                username=user.username,
                email=user.email,
                password=get_password_hash(user.password))
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
