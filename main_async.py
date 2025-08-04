import time
import asyncio
from fastapi import FastAPI, BackgroundTasks

app = FastAPI()


def sync_task():
    time.sleep(3)
    print('отправлено письмо')


async def async_task():
    await asyncio.sleep(3)
    print('запрос в сторонний АПИ')


@app.post('/')
async def some_route(bg_tasks: BackgroundTasks):
    ...
    # asyncio.create_task(async_task())
    bg_tasks.add_task(sync_task)
    return 'ok'
