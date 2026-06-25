from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    APP_MODE: str = "desktop"
    DATABASE_URL: str = "sqlite:///kanban.db"

    # Нові змінні для конфігурації мережі
    BACKEND_HOST: str = "127.0.0.1"
    BACKEND_PORT: int = 8000

    # Реєструємо префікс
    API_V1_STR: str = "/api/v1"

    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", extra="ignore"
    )


settings = Settings()
