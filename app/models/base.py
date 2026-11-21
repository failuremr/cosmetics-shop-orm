from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    """Базовый класс для всех моделей — Alembic ориентируется на его metadata."""
    pass
