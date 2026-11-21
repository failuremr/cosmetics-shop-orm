from datetime import datetime

from sqlalchemy import Float, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base


class Recommendation(Base):
    """
    Персональная рекомендация товара клиенту — результат работы системы
    рекомендаций на основе конкретного анализа кожи.
    """

    __tablename__ = "recommendations"

    id: Mapped[int] = mapped_column(primary_key=True)
    analysis_id: Mapped[int] = mapped_column(ForeignKey("skin_analyses.id"))
    product_id: Mapped[int] = mapped_column(ForeignKey("products.id"))
    relevance_score: Mapped[float] = mapped_column(Float)  # 0..1 — насколько товар подходит
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    analysis: Mapped["SkinAnalysis"] = relationship(back_populates="recommendations")
    product: Mapped["Product"] = relationship(back_populates="recommendations")

    def __repr__(self) -> str:
        return f"Recommendation(analysis_id={self.analysis_id}, product_id={self.product_id}, score={self.relevance_score})"
