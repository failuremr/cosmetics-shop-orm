from typing import List, Optional

from sqlalchemy import String, Float, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base


class Product(Base):
    """Товар (косметическое средство)."""

    __tablename__ = "products"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(150))
    category: Mapped[str] = mapped_column(String(50))  # очищение / увлажнение / защита от солнца и т.д.
    price: Mapped[float] = mapped_column(Float)
    # под какой тип кожи подходит: сухая / жирная / комбинированная / нормальная / чувствительная
    suitable_skin_type: Mapped[str] = mapped_column(String(50))
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    recommendations: Mapped[List["Recommendation"]] = relationship(
        back_populates="product", cascade="all, delete-orphan"
    )

    def __repr__(self) -> str:
        return f"Product(id={self.id}, name={self.name!r}, price={self.price})"
