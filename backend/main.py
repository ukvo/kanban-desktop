from contextlib import asynccontextmanager
from fastapi import FastAPI
from loguru import logger

from app.api.routers import project, status
from app.core.db import init_db


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Ініціалізація бази даних SQLite...")
    init_db()
    logger.info("Базу даних успішно ініціалізовано з дефолтними статусами!")
    yield
    logger.info("Зупинка сервера...")


app = FastAPI(title="Kanban Local Backend", lifespan=lifespan)

logger.add("logs/app.log", rotation="10 MB", retention="10 days", compression="zip")

# Підключаємо наші API-маршрутизатори
app.include_router(project.router)
app.include_router(status.router)


@app.get("/")
def read_root():
    return {"status": "working", "mode": "desktop"}
