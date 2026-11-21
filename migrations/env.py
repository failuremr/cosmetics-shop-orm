from logging.config import fileConfig

from sqlalchemy import engine_from_config
from sqlalchemy import pool

from alembic import context

# добавляем модели, чтобы Alembic видел их metadata для автогенерации
from app.models import Base  # noqa: E402

# объект конфигурации Alembic, предоставляет доступ к значениям из alembic.ini
config = context.config

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# metadata наших моделей - по ней alembic revision --autogenerate сравнивает
# текущее состояние БД с описанными моделями
target_metadata = Base.metadata


def run_migrations_offline() -> None:
    """Запуск миграций в 'offline'-режиме (генерирует SQL без подключения к БД)."""
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Запуск миграций в 'online'-режиме (с реальным подключением к БД)."""
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
