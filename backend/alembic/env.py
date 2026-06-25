from logging.config import fileConfig

from alembic import context
from sqlmodel import SQLModel

# Імпортуємо наш конфіг із налаштуваннями з .env
from app.core.config import settings

# КРИТИЧНО ВАЖЛИВО: імпортуємо файл моделей, щоб Python завантажив класи таблиць у пам'ять,
# інакше SQLModel.metadata залишиться порожнім для Alembic

# Це стандартний об'єкт конфігурації Alembic, який надає
# доступ до значень всередині файлу alembic.ini.
config = context.config

# Інтерпретуємо конфігураційний файл для логування (налаштування з alembic.ini)
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Передаємо об'єкт метаданих SQLModel для підтримки автогенерації міграцій
target_metadata = SQLModel.metadata


def run_migrations_offline() -> None:
    """Запуск міграцій в 'offline' режимі.

    Тут нам потрібен лише URL бази даних. Контекст налаштовується без створення двигуна (Engine).
    """
    # Динамічно підставляємо URL бази даних з нашого файлу settings
    url = settings.DATABASE_URL
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Запуск міграцій в 'online' режимі (з підключенням до реальної бази даних)."""
    from sqlmodel import create_engine

    # Створюємо підключення динамічно на основі нашого settings.DATABASE_URL
    connect_args = {}
    if settings.DATABASE_URL.startswith("sqlite"):
        connect_args = {"check_same_thread": False}

    connectable = create_engine(settings.DATABASE_URL, connect_args=connect_args)

    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata, user_module_prefix="sqlmodel.")

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
