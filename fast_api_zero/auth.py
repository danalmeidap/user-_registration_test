from fastapi import APIRouter, Depends, HTTPException, status

from fast_api_zero.schemas import LoginRequest, UserDB
from fast_api_zero.security import verify_password
from fast_api_zero.user_repository import UserRepository
from fast_api_zero.users import get_user_repository

auth_router = APIRouter()


@auth_router.post('/login', response_model=UserDB)
def login(
    login_request: LoginRequest,
    repository: UserRepository = Depends(get_user_repository)
):
    user = repository.get_user_by_email(login_request.email)
    if user and verify_password(login_request.password, user.password):
        return user
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail='Invalid credentials',
    )
