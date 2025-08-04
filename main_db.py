from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import select

from fastapi import FastAPI, Depends
from pydantic import BaseModel, Field
from typing import Annotated


app = FastAPI()

engine = create_async_engine('sqlite+aiosqlite:///books.db')

new_session = async_sessionmaker(engine, expire_on_commit=False)


async def get_session():
    """Создание сессии"""
    async with new_session() as session:
        yield session   # отдаёт сессию на время работы ручки


SessionDep = Annotated[AsyncSession, Depends(get_session)]
# валидация переданных данных, проброс зависимостей (можно и без этого)


class Base(DeclarativeBase):
    pass


class BookModel(Base):
    """Создание/валидация таблицы"""
    __tablename__ = 'books'
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str]
    author: Mapped[str]


@app.post('/setup_database', summary='Создать БД', tags=['Создать БД 💽'])
async def setup_database():
    """Создаём соединение с БД и таблицы"""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)     # очистим базу
        await conn.run_sync(Base.metadata.create_all)   # добавим таблицы
    return 'ok'


class BookAddSchema(BaseModel):
    title: str
    author: str


class BookSchema(BookAddSchema):
    id: int


class PaginationParams(BaseModel):
    limit: int = Field(5, description='Кол-во элементов на странице')
    offset: int = Field(0, description='Смещение для пагинации')


# Пагинация: чего по сколько показывать в запросе. Можно сиспользовать, можно - нет.
# Depends - функция для управления внедрением зависимостей
PaginationDep = Annotated[PaginationParams, Depends(PaginationParams)]


@app.post('/books', summary='Добавить', tags=['Добавить книги 📚'])
async def add_books(data: BookAddSchema, session: SessionDep):
    """Добавить книги"""
    new_book = BookModel(title=data.title, author=data.author)  # запрос на добавление через ORM
    session.add(new_book)   # добавить книгу
    await session.commit()
    return 'ok'


# @app.get('/books', summary='Показать', tags=['Показать книги 📚'])
# async def get_books(session: SessionDep):
#     """Показать книги"""
#     query = select(BookModel)   # выбрать через stlect
#     result = await session.execute(query)   # исполнить запрос
#     return result.scalars().all()   # вернуть (все записи)


@app.get('/books', summary='Показать', tags=['Показать книги 📚'])
async def get_books(session: SessionDep,
                    pagination: PaginationDep):
    """Показать книги. Установим лимит, а также интервал"""
    query = select(BookModel).limit(pagination.limit).offset(pagination.offset)
    result = await session.execute(query)
    return result.scalars().all()
