# https://www.youtube.com/watch?v=xb_jtnYiPUQ&list=PLOQgLBuj2-3IuFbt-wJw2p2NiV9WTRzIP&index=13
# olhar o parametrize para os testes
# corrigir a rota get do TODOS
from http import HTTPStatus

from fastapi import FastAPI

from fast_api.routers import auth, todo, users
from fast_api.schemas import Message

app = FastAPI()
app.include_router(users.router)
app.include_router(auth.router)
app.include_router(todo.router)


@app.get('/', status_code=HTTPStatus.OK, response_model=Message)
def red_root():
    return {'message': 'Olá Mundo!'}
