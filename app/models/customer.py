from datetime import datetime
from typing import List

from sqlalchemy import String, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base


class Customer(Base):
    """Клиент интернет-магазина косметики."""

    __tablename__ = "customers"

    id: Mapped[int] = mapped_column(primary_key=True)
    full_name: Mapped[str] = mapped_column(String(100))
    email: Mapped[str] = mapped_column(String(120), unique=True)
    registered_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    skin_analyses: Mapped[List["SkinAnalysis"]] = relationship(
        back_populates="customer", cascade="all, delete-orphan"
    )

    def __repr__(self) -> str:
        return f"Customer(id={self.id}, full_name={self.full_name!r}, email={self.email!r})"
