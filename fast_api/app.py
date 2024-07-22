# https://youtu.be/nGqvdJ4Z-iA?t=961 2306
from http import HTTPStatus

from fastapi import FastAPI

from fast_api.routers import auth, users
from fast_api.schemas import Message

app = FastAPI()
app.include_router(users.router)
app.include_router(auth.router)


@app.get('/', status_code=HTTPStatus.OK, response_model=Message)
def red_root():
    return {'message': 'Olá Mundo!'}
