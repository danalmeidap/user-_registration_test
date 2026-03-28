from fastapi import FastAPI, status

from fast_api_zero.database import engine
from fast_api_zero.models import table_registry
from fast_api_zero.users import router

app = FastAPI()
app.include_router(router, prefix='/users', tags=['users'])
table_registry.metadata.create_all(bind=engine)


@app.get('/', status_code=status.HTTP_200_OK)
def read_root() -> dict[str, str]:
    return {'message': 'Hello World'}
