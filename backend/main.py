from contextlib import asynccontextmanager
from fastapi import FastAPI
from loguru import logger

from app.core.db import init_db
from app.models.models import (
    Project,
    Status,
)  # Імпортуємо, щоб SQLModel побачив таблиці


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Цей код виконується ПЕРЕД запуском сервера
    logger.info("Ініціалізація бази даних SQLite...")
    init_db()
    logger.info("Базу даних успішно ініціалізовано!")
    yield
    # Цей код виконається при зупинці сервера
    logger.info("Зупинка сервера...")


app = FastAPI(title="Kanban Local Backend", lifespan=lifespan)

# Налаштовуємо логування у файл
logger.add("logs/app.log", rotation="10 MB", retention="10 days", compression="zip")


@app.get("/")
def read_root():
    return {"status": "working", "mode": "desktop"}
