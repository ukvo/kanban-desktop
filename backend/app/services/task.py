from datetime import datetime, timezone
from typing import Optional, Sequence
from sqlmodel import Session, select, col
from loguru import logger
from app.models.models import Task


def create_task(
    session: Session,
    project_id: int,
    status_id: int,
    title: str,
    description: Optional[str] = None,
    priority: int = 2,
) -> Task:
    """Створення нової картки задачі"""
    logger.info(f"Створення задачі '{title}' у проекті {project_id}")
    db_task = Task(
        project_id=project_id,
        status_id=status_id,
        title=title,
        description=description,
        priority=priority,
    )
    session.add(db_task)
    session.commit()
    session.refresh(db_task)
    return db_task


def get_tasks_by_project(session: Session, project_id: int, status_id: Optional[int] = None) -> Sequence[Task]:
    """Отримання списку задач проекту з автоматичним сортуванням за пріоритетом та часом оновлення"""
    statement = select(Task).where(Task.project_id == project_id)

    if status_id:
        statement = statement.where(Task.status_id == status_id)

    # Сортування: Спочатку пріоритет (3 -> 1), потім дата оновлення (найновіші вгорі)
    statement = statement.order_by(col(Task.priority).desc(), col(Task.updated_at).desc())
    return session.exec(statement).all()


def update_task_status_or_priority(
    session: Session,
    task_id: int,
    status_id: Optional[int] = None,
    priority: Optional[int] = None,
) -> Optional[Task]:
    """Оновлення колонки або пріоритету задачі (використовується при Drag & Drop картки)"""
    db_task = session.get(Task, task_id)
    if not db_task:
        return None

    if status_id is not None:
        db_task.status_id = status_id
    if priority is not None:
        db_task.priority = priority

    # Критично для синхронізації: оновлюємо мітку часу будь-якої зміни
    db_task.updated_at = datetime.now(timezone.utc)

    session.add(db_task)
    session.commit()
    session.refresh(db_task)
    return db_task


def delete_task(session: Session, task_id: int) -> bool:
    """Видалення картки задачі (Soft/Hard в залежності від логіки очищення кошика)"""
    db_task = session.get(Task, task_id)
    if not db_task:
        return False
    session.delete(db_task)
    session.commit()
    return True
