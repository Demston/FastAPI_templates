from pydantic import BaseModel, Field, ConfigDict
from fastapi import FastAPI

app = FastAPI()

data = {
    'bio': 'Дружок-Пирожок',
    'age': 35
}


class UserSchema(BaseModel):
    bio: str | None = Field(max_length=100)
    age: int = Field(ge=0, le=130)
    model_config = ConfigDict(extra='forbid')   # защита от левых данных, запрет доп. параметров


users = []


@app.post('/users')
def add_user(user: UserSchema):
    users.append(user)
    return {'ok': True, 'msg': 'Юзер добавлен'}


@app.get('/users')
def get_users() -> list[UserSchema]:
    return users


# user = UserSchema(**data)
# print(repr(user))
