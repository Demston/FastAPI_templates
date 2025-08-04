from fastapi import FastAPI, HTTPException, Request
import uvicorn
from pydantic import BaseModel
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()     # Запуск: uvicorn main:app --reload
# Проверка - запросы исключительно с этого адреса
app.add_middleware(CORSMiddleware, allow_origins=['http://127.0.0.1:8000'])

# Настройка статических файлов (css, js, изображения)
# app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")  # Настройка Jinja2

books = [
    {
        'id': 1,
        'title': 'Асинхронность в Питоне',
        'author': 'Mathew'
    },
    {
        'id': 2,
        'title': 'Разработка на Питоне',
        'author': 'Dmitry'
    }
]


@app.get('/', response_class=HTMLResponse)
async def read_root(request: Request):
    """Обработчик корневого URL"""
    return templates.TemplateResponse("index.html", {"request": request, "books": books})


@app.get('/books', summary='Получить книги', tags=['Получить книги 📚'])
def read_books():
    return books


@app.get('/books/{book_id}', summary='Получить книгу', tags=['нига'])
def get_book(book_id: int):
    for b in books:
        if b['id'] == book_id:
            return b
    raise HTTPException(status_code=404, detail='нет книги')


class NewBook(BaseModel):
    title: str
    author: str


@app.post('/books', summary='Добавить ниги', tags=['Добавить ниги 📚'])
def create_book(new_book: NewBook):
    books.append({'id': len(books)+1,
                  'title': new_book.title,
                  'author': new_book.author})
    return {'success': True, 'message': 'Книга добавлена'}


if __name__ == '__main__':
    uvicorn.run('main:app', reload=True)
