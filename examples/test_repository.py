"""
Ручная проверка репозитория (п.10 задания: "класс для тестирования, где
дёргаете методы репозитория для выполнения операций над данными").

Запуск из корня проекта (после `alembic upgrade head`):
    python -m examples.test_repository
"""
from app.database import SessionLocal
from app.models import Customer, SkinAnalysis, Recommendation
from app.repositories import ProductRepository


def main() -> None:
    session = SessionLocal()
    repo = ProductRepository(session)

    print("--- CREATE ---")
    p1 = repo.create(
        name="Увлажняющая сыворотка с гиалуроновой кислотой",
        category="сыворотка",
        price=1290.0,
        suitable_skin_type="сухая",
        description="Интенсивное увлажнение",
    )
    p2 = repo.create(
        name="Матирующий крем для жирной кожи",
        category="крем",
        price=890.0,
        suitable_skin_type="жирная",
    )
    p3 = repo.create(
        name="Тонер для комбинированной кожи",
        category="тонер",
        price=650.0,
        suitable_skin_type="комбинированная",
    )
    print(p1, p2, p3, sep="\n")

    print("\n--- GET_ALL ---")
    for product in repo.get_all():
        print(product)

    print("\n--- GET_BY_ID ---")
    print(repo.get_by_id(p1.id))

    print("\n--- GET_BY_SKIN_TYPE('жирная') ---")
    for product in repo.get_by_skin_type("жирная"):
        print(product)

    print("\n--- UPDATE (меняем цену p1) ---")
    updated = repo.update(p1.id, price=1190.0)
    print(updated)

    print("\n--- DELETE (удаляем p2) ---")
    deleted = repo.delete(p2.id)
    print("Удалено:", deleted)
    print("Осталось товаров:", len(repo.get_all()))

    print("\n--- Демонстрация связанных сущностей (Customer -> SkinAnalysis -> Recommendation -> Product) ---")
    customer = Customer(full_name="Иванова Мария", email="ivanova@example.com")
    session.add(customer)
    session.commit()
    session.refresh(customer)

    analysis = SkinAnalysis(
        customer_id=customer.id,
        skin_type="комбинированная",
        detected_issues="пигментация, расширенные поры",
        photo_path="/uploads/face1.jpg",
    )
    session.add(analysis)
    session.commit()
    session.refresh(analysis)

    for product in repo.get_by_skin_type("комбинированная"):
        session.add(
            Recommendation(analysis_id=analysis.id, product_id=product.id, relevance_score=0.9)
        )
    session.commit()

    print(f"Клиент: {customer}")
    print(f"Анализ кожи: {analysis}")
    print("Рекомендованные товары:")
    for rec in analysis.recommendations:
        print(f"  - {rec.product.name} (score={rec.relevance_score})")

    session.close()


if __name__ == "__main__":
    main()
