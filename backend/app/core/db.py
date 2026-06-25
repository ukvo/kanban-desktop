from sqlmodel import Session, SQLModel, create_engine
from app.core.config import settings

# Зчитуємо URL бази даних безпосередньо з налаштувань .env
sqlite_url = settings.DATABASE_URL

# Конфігурація потоків потрібна тільки якщо ми використовуємо SQLite
connect_args = {}
if sqlite_url.startswith("sqlite"):
    connect_args = {"check_same_thread": False}

engine = create_engine(sqlite_url, connect_args=connect_args)


def init_db():
    """Функція для створення всіх таблиць при старті додатка"""
    SQLModel.metadata.create_all(engine)


def get_session():
    """Функція-генератор (Dependency) для отримання сесії БД у маршрутах FastAPI"""
    with Session(engine) as session:
        yield session
