from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # Змінні автоматично зчитаються з .env. Якщо файлу немає — візьмуться значення за дефолтом
    APP_MODE: str = "desktop"
    DATABASE_URL: str = "sqlite:///kanban.db"

    # Налаштування pydantic для роботи з файлом .env
    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", extra="ignore"
    )


# Створюємо єдиний екземпляр налаштувань для всього додатка
settings = Settings()
