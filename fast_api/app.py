# https://youtu.be/JzJYWQ6wBAE?list=PLOQgLBuj2-3IuFbt-wJw2p2NiV9WTRzIP&t=4661
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
