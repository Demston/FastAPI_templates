from fastapi import FastAPI, HTTPException
import uvicorn
from pydantic import BaseModel

app = FastAPI()
# uvicorn main:app --reload

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


@app.post('/books', summary='Добавить ниги', tags=['Добавить книги 📚'])
def create_book(new_book: NewBook):
    books.append({'id': len(books)+1,
                  'title': new_book.title,
                  'author': new_book.author})
    return {'success': True, 'message': 'Книга добавлена'}


if __name__ == '__main__':
    uvicorn.run('main:app', reload=True)
