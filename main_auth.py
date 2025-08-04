from fastapi import FastAPI, HTTPException, Response, Depends
from authx import AuthX, AuthXConfig
from pydantic import BaseModel

app = FastAPI()

config = AuthXConfig()
config.JWT_SECRET_KEY = 'SECRET_KEY'
config.JWT_ACCESS_COOKIE_NAME = 'my_access_token'   # произвольное имя
config.JWT_TOKEN_LOCATION = ['cookies']     # работа с куками (можно выбрать с заголовками)

security = AuthX(config=config)


class UserLoginSchema(BaseModel):
    username: str
    password: str


@app.post('/login')
def login(creds: UserLoginSchema, responce: Response):
    """Авторизация"""
    if creds.username == 'test' and creds.password == 'test':
        token = security.create_access_token(uid='12456')
        responce.set_cookie(config.JWT_ACCESS_COOKIE_NAME, token)   # добавляем куки в запрос
        return {'access token': token}
    raise HTTPException(status_code=401, detail='Incorrect login or password mazafaka')


@app.get('/protected', dependencies=[Depends(security.access_token_required)])  # проверка авторизации
def protected():
    """Получение данных авторизованным/неавторизованным пользователем"""
    return {'data': 'ToP SecreT'}
