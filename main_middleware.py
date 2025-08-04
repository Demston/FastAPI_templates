"""Middleware в FastAPI нужен для того, чтобы запускать код перед и после каждого запроса.
Это позволяет добавлять пользовательскую логику в жизненный цикл каждого запроса.

Некоторые области применения middleware:

- Аутентификация и авторизация. Обеспечение доступа только для аутентифицированных пользователей к
определённым конечным точкам.
- Логгирование. Отслеживание входящих запросов и исходящих ответов для отладки или мониторинга.
- Ограничение количества запросов. Контроль числа запросов, которые клиент может сделать в определённый период.
- Трансформация запросов и ответов. Изменение запросов до того, как они достигнут обработчиков маршрута,
или ответов перед отправкой их клиенту."""

from fastapi import FastAPI, Request, Response
from typing import Callable
import uvicorn
import time

app = FastAPI()
# uvicorn main:app --reload


@app.middleware('http')     # вставим что-нибудь между функцией и самим запросом
async def my_middle(request: Request, call_next: Callable):
    start = time.perf_counter()     # запустим счётчик для примера
    response = await call_next(request)
    end = time.perf_counter() - start
    print(f'время обработки запроса: {end}')
    response.headers['Anything'] = 'Yo man!'    # передадим ещё и заголовок
    return response


@app.get('/users', tags=['Пользователи'])
async def get_users():
    time.sleep(1)
    return [{'id': 1, 'name': 'Dima'}]


if __name__ == '__main__':
    uvicorn.run('main:app', reload=True)
