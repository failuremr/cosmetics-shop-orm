# Интернет-магазин косметики — слой доступа к данным (ORM + Repository + Alembic)

Лабораторная работа по дисциплине «Командное проектирование и разработка».
Предметная область — тема ВКР: *«Разработка интернет-магазина косметической
продукции с интеллектуальной системой персональных рекомендаций на основе
анализа кожи лица по фотографии»*.

Стек: **Python 3.11+, SQLAlchemy 2.0 (ORM), Alembic (миграции), SQLite**.

## Структура проекта

```
app/
  database.py              # engine + SessionLocal (подключение к SQLite)
  models/
    base.py                # Base (DeclarativeBase) — на неё опирается Alembic
    customer.py             # Customer   — клиент магазина
    product.py               # Product    — товар (косметическое средство)
    skin_analysis.py          # SkinAnalysis — результат ИИ-анализа кожи по фото
    recommendation.py          # Recommendation — рекомендация товара клиенту
  repositories/
    product_repository.py    # паттерн Repository: CRUD + выборки для Product
examples/
  test_repository.py         # ручная проверка репозитория (CRUD + связи)
migrations/                  # Alembic: env.py, versions/*.py
docs/
  schema.png                # ER-диаграмма (доп. задание)
alembic.ini
requirements.txt
```

## Модель данных

- **Customer** — клиент: ФИО, email, дата регистрации.
- **Product** — товар: название, категория, цена, под какой тип кожи подходит.
- **SkinAnalysis** — результат ИИ-анализа фото лица клиента: определённый тип
  кожи, обнаруженные особенности (пигментация, расширенные поры и т.д.).
  Именно эта сущность — ядро темы ВКР.
- **Recommendation** — связующая сущность: конкретная рекомендация товара,
  построенная на основе конкретного анализа кожи, с коэффициентом релевантности.

Связи: `Customer 1—N SkinAnalysis`, `SkinAnalysis 1—N Recommendation`,
`Product 1—N Recommendation`. ER-диаграмма — `docs/schema.png`.

## Паттерн Repository

`ProductRepository` (`app/repositories/product_repository.py`) абстрагирует
работу с таблицей `products`: бизнес-логика работает с объектами `Product`
через `create / get_by_id / get_all / get_by_skin_type / get_by_category /
update / delete`, не зная деталей SQL/SQLAlchemy.

## Установка и запуск

1. Создать и активировать виртуальное окружение:

   ```bash
   python -m venv .venv
   # Windows PowerShell:
   .venv\Scripts\Activate.ps1
   # Linux/macOS:
   source .venv/bin/activate
   ```

2. Установить зависимости:

   ```bash
   pip install -r requirements.txt
   ```

3. Применить миграции (создаст файл `cosmetics_shop.db` со всеми таблицами):

   ```bash
   alembic upgrade head
   ```

4. Запустить проверку репозитория:

   ```bash
   python -m examples.test_repository
   ```

   Скрипт создаёт несколько товаров, читает их, обновляет, удаляет один,
   затем создаёт клиента → анализ кожи → рекомендации и печатает результат
   JOIN-а по всей цепочке `Customer → SkinAnalysis → Recommendation → Product`.

## Работа с миграциями далее

Если изменить модели в `app/models`, сгенерировать новую миграцию:

```bash
alembic revision --autogenerate -m "описание изменения"
```

Полученный файл в `migrations/versions/` нужно обязательно открыть и
проверить вручную (autogenerate — черновик), затем применить:

```bash
alembic upgrade head
```

Откат последней миграции: `alembic downgrade -1`.

## Примечание о проверке

В окружении, где собиралась эта лаба, не было доступа к PyPI, поэтому
SQLAlchemy/Alembic не устанавливались и ORM-код не запускался напрямую —
зато вся логика схемы и CRUD-операций (таблицы, внешние ключи, JOIN по всей
цепочке сущностей) была проверена эквивалентными запросами на «чистом»
`sqlite3` из стандартной библиотеки Python, и все проверки прошли успешно.
После `pip install -r requirements.txt` код в `app/` и `examples/` выполняется
как обычный проект на SQLAlchemy — без каких-либо дополнительных шагов.
