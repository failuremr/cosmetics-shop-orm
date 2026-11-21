"""
Подключение к базе данных.
Используется SQLite — не требует отдельного сервера, удобно для лабораторной.
engine создаёт соединения, SessionLocal — фабрика сессий (Unit of Work из ORM).
"""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "sqlite:///cosmetics_shop.db"

engine = create_engine(DATABASE_URL, echo=False)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)
