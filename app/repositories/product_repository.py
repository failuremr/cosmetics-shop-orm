"""
Паттерн Repository для сущности Product.

Репозиторий прячет от бизнес-логики то, как именно данные хранятся и
извлекаются (SQLAlchemy/SQL), и предоставляет понятный набор методов —
как если бы это была обычная коллекция объектов в памяти.
"""
from typing import List, Optional

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.product import Product


class ProductRepository:
    def __init__(self, session: Session):
        self.session = session

    def create(
        self,
        name: str,
        category: str,
        price: float,
        suitable_skin_type: str,
        description: Optional[str] = None,
    ) -> Product:
        product = Product(
            name=name,
            category=category,
            price=price,
            suitable_skin_type=suitable_skin_type,
            description=description,
        )
        self.session.add(product)
        self.session.commit()
        self.session.refresh(product)
        return product

    def get_by_id(self, product_id: int) -> Optional[Product]:
        return self.session.get(Product, product_id)

    def get_all(self) -> List[Product]:
        return list(self.session.scalars(select(Product)).all())

    def get_by_skin_type(self, skin_type: str) -> List[Product]:
        """Доп. метод: товары, подходящие под конкретный тип кожи."""
        stmt = select(Product).where(Product.suitable_skin_type == skin_type)
        return list(self.session.scalars(stmt).all())

    def get_by_category(self, category: str) -> List[Product]:
        stmt = select(Product).where(Product.category == category)
        return list(self.session.scalars(stmt).all())

    def update(self, product_id: int, **fields) -> Optional[Product]:
        product = self.get_by_id(product_id)
        if product is None:
            return None
        for key, value in fields.items():
            setattr(product, key, value)
        self.session.commit()
        self.session.refresh(product)
        return product

    def delete(self, product_id: int) -> bool:
        product = self.get_by_id(product_id)
        if product is None:
            return False
        self.session.delete(product)
        self.session.commit()
        return True
