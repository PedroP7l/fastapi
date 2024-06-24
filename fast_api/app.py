from http import HTTPStatus

from fastapi import FastAPI

from fast_api.schemas import Message

app = FastAPI()


@app.get('/', status_code=HTTPStatus.OK, response_model=Message)
def red_root():
    return {'message': 'Olá Mundo!'}
