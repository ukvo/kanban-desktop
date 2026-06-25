from datetime import datetime, timezone
from typing import Optional
from sqlmodel import Field, SQLModel


# Спільний базовий клас, щоб автоматично додавати час створення до таблиць
class TimestampModel(SQLModel):
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        nullable=False,
    )


class Project(TimestampModel, table=True):
    """Таблиця проектів (Контексти дошок)"""

    __tablename__ = "projects"

    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True, nullable=False)
    description: Optional[str] = Field(default=None)


class Status(SQLModel, table=True):
    """Таблиця колонок / статусів на Kanban-дошці"""

    __tablename__ = "statuses"

    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(nullable=False)
    group: str = Field(default="active", nullable=False)  # active, archived, deleted
    position: int = Field(default=0, nullable=False)  # порядок зліва направо
