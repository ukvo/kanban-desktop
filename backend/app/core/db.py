from sqlmodel import Session, SQLModel, create_engine

# Ім'я файлу бази даних SQLite, який створиться автоматично в папці backend
sqlite_file_name = "kanban.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

# check_same_thread=False потрібен тільки для SQLite, бо FastAPI працює в кілька потоків
connect_args = {"check_same_thread": False}
engine = create_engine(sqlite_url, connect_args=connect_args)


def init_db():
    """Функція для створення всіх таблиць при старті додатка"""
    SQLModel.metadata.create_all(engine)


def get_session():
    """Функція-генератор (Dependency) для отримання сесії БД у маршрутах FastAPI"""
    with Session(engine) as session:
        yield session
