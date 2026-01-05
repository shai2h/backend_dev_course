from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy import text
from src.config import settings
from sqlalchemy.orm import DeclarativeBase


# engine не делает запросы, раздает соединения
engine = create_async_engine(settings.DB_URL) # подключение к базе данных, можно использовать echo=True для небольшого логирования

"""
engine - хранит пул соеднинений
session - берет одно соединение из пула и работает через него
"""

async_session_maker = async_sessionmaker(bind=engine, expire_on_commit=False)


class Base(DeclarativeBase):
    pass