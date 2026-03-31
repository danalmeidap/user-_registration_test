from fastapi import FastAPI, status

from fast_api_zero.auth import auth_router
from fast_api_zero.database import engine
from fast_api_zero.models import table_registry
from fast_api_zero.users import user_router

app = FastAPI()
app.include_router(user_router, prefix='/users', tags=['users'])
app.include_router(auth_router, prefix='/auth', tags=['auth'])
table_registry.metadata.create_all(bind=engine)


@app.get('/', status_code=status.HTTP_200_OK)
def read_root() -> dict[str, str]:
    return {'message': 'Hello World'}
