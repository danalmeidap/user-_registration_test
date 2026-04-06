from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from fast_api_zero.schemas import Token
from fast_api_zero.security import verify_password
from fast_api_zero.token import create_access_token
from fast_api_zero.user_repository import UserRepository
from fast_api_zero.users import get_user_repository

auth_router = APIRouter()


@auth_router.post('', response_model=Token)
def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    repository: Annotated[UserRepository, Depends(get_user_repository)],
):
    user = repository.get_user_by_username(form_data.username)
    if user and verify_password(form_data.password, user.password):
        token = create_access_token(data={'sub': user.username})
        return {'access_token': token, 'token_type': 'bearer'}
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='User not found',
        )
    if not verify_password(form_data.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Invalid credentials',
            headers={'WWW-Authenticate': 'bearer'},
        )
