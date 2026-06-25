from fastapi import FastAPI
from loguru import logger

app = FastAPI(title="Kanban Local Backend")

# Налаштовуємо логування у файл
logger.add("logs/app.log", rotation="10 MB", retention="10 days", compression="zip")

@app.get("/")
def read_root():
    logger.info("Тестовий запит до кореневого ендпоінту")
    return {"status": "working", "mode": "desktop"}
