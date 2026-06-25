from datetime import datetime, timezone
from typing import List, Optional
from sqlmodel import Field, Relationship, SQLModel


# Спільний базовий клас для дат створення
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

    # Зв'язок: Один проект має багато задач
    tasks: List["Task"] = Relationship(
        back_populates="project", cascade_delete=True
    )


class Status(SQLModel, table=True):
    """Таблиця колонок / статусів на Kanban-дошці"""

    __tablename__ = "statuses"

    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(nullable=False)
    group: str = Field(default="active", nullable=False)  # active, archived, deleted
    position: int = Field(default=0, nullable=False)

    # Зв'язок: Один статус має багато задач
    tasks: List["Task"] = Relationship(back_populates="status")


class Task(TimestampModel, table=True):
    """Центральна таблиця карток задач"""

    __tablename__ = "tasks"

    id: Optional[int] = Field(default=None, primary_key=True)
    title: str = Field(nullable=False)
    description: Optional[str] = Field(default=None)
    priority: int = Field(default=2, nullable=False)  # 1-Low, 2-Medium, 3-High

    # Обов'язкове поле для синхронізації з хмарою (оновлюється при будь-якому сейві)
    updated_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        nullable=False,
    )

    # Зовнішні ключі (Foreign Keys)
    project_id: int = Field(
        foreign_key="projects.id", ondelete="CASCADE", index=True
    )
    status_id: int = Field(
        foreign_key="statuses.id", ondelete="RESTRICT", index=True
    )

    # Об'єкти зв'язків ORM (для зручного підтягування даних через API)
    project: Project = Relationship(back_populates="tasks")
    status: Status = Relationship(back_populates="tasks")

    # Зв'язок з підзадачами: Одна задача має багато підзадач (чек-ліст)
    subtasks: List["Subtask"] = Relationship(
        back_populates="task", cascade_delete=True
    )


class Subtask(TimestampModel, table=True):
    """Таблиця пунктів чек-ліста (підзадач)"""

    __tablename__ = "subtasks"

    id: Optional[int] = Field(default=None, primary_key=True)
    text: str = Field(nullable=False)
    is_done: bool = Field(default=False, nullable=False)
    due_date: Optional[datetime] = Field(default=None, nullable=True)  # дедлайн пункта

    # Зовнішній ключ на батьківську задачу
    task_id: int = Field(foreign_key="tasks.id", ondelete="CASCADE", index=True)

    # Зв'язок назад до задачі
    task: Task = Relationship(back_populates="subtasks")
