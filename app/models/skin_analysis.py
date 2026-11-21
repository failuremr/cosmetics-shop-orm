from datetime import datetime
from typing import List, Optional

from sqlalchemy import String, Text, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base


class SkinAnalysis(Base):
    """
    Результат ИИ-анализа кожи лица по фотографии клиента.
    Это и есть ядро темы ВКР — на основе этой записи строятся рекомендации товаров.
    """

    __tablename__ = "skin_analyses"

    id: Mapped[int] = mapped_column(primary_key=True)
    customer_id: Mapped[int] = mapped_column(ForeignKey("customers.id"))
    skin_type: Mapped[str] = mapped_column(String(50))  # результат, который определил ИИ
    # проблемные зоны/особенности через запятую, например: "пигментация, расширенные поры"
    detected_issues: Mapped[str] = mapped_column(Text)
    photo_path: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    analyzed_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    customer: Mapped["Customer"] = relationship(back_populates="skin_analyses")
    recommendations: Mapped[List["Recommendation"]] = relationship(
        back_populates="analysis", cascade="all, delete-orphan"
    )

    def __repr__(self) -> str:
        return f"SkinAnalysis(id={self.id}, customer_id={self.customer_id}, skin_type={self.skin_type!r})"
