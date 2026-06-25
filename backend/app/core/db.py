from sqlmodel import Session, SQLModel, create_engine, select

from app.core.config import settings
from app.models.models import Status

sqlite_url = settings.DATABASE_URL

connect_args = {}
if sqlite_url.startswith("sqlite"):
    connect_args = {"check_same_thread": False}

engine = create_engine(sqlite_url, connect_args=connect_args)


def init_db():
    """Створення таблиць та наповнення дефолтними даними при першому старті"""
    SQLModel.metadata.create_all(engine)

    # Додаємо стандартні колонки для Kanban-дошки, якщо таблиця порожня
    with Session(engine) as session:
        statement = select(Status)
        existing_statuses = session.exec(statement).first()

        if not existing_statuses:
            default_columns = [
                Status(name="Backlog", group="active", position=0),
                Status(name="In Progress", group="active", position=1),
                Status(name="Done", group="active", position=2),
            ]
            session.add_all(default_columns)
            session.commit()


def get_session():
    """Функція-генератор для отримання сесії БД у маршрутах FastAPI"""
    with Session(engine) as session:
        yield session
