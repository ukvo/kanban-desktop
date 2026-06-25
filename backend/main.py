from contextlib import asynccontextmanager
from fastapi import FastAPI
from loguru import logger

from app.core.config import settings
from app.api.routers import project, status, task, subtask


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Перевірка та ініціалізація дефолтних статусів...")

    # Викликаємо ініціалізацію дефлтних статусів (вона тепер безпечна,
    # бо таблиці вже мають бути створені міграціями)
    from app.core.db import init_db

    init_db()  # Тут всередині db.py зараз залишиться тільки перевірка дефолтних статусів

    logger.info("Бекенд успішно запущено!")
    yield
    logger.info("Зупинка сервера...")


app = FastAPI(title="Kanban Local Backend", lifespan=lifespan)

logger.add("logs/app.log", rotation="10 MB", retention="10 days", compression="zip")

# Підключаємо наші API-маршрутизатори
app.include_router(project.router, prefix=settings.API_V1_STR)
app.include_router(status.router, prefix=settings.API_V1_STR)
app.include_router(task.router, prefix=settings.API_V1_STR)
app.include_router(subtask.router, prefix=settings.API_V1_STR)


@app.get("/")
def read_root():
    return {"status": "working", "mode": "desktop"}
