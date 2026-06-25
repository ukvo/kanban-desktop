from datetime import datetime, timezone
from typing import Optional
from sqlmodel import Session
from app.models.models import Subtask, Task


def create_subtask(
    session: Session, task_id: int, text: str, due_date: Optional[datetime] = None
) -> Optional[Subtask]:
    """Додавання нового пункту в чек-ліст задачі"""
    db_task = session.get(Task, task_id)
    if not db_task:
        return None

    db_subtask = Subtask(task_id=task_id, text=text, due_date=due_date)
    session.add(db_subtask)

    # Оновлюємо мітку часу батьківської задачі
    db_task.updated_at = datetime.now(timezone.utc)
    session.add(db_task)

    session.commit()
    session.refresh(db_subtask)
    return db_subtask


def toggle_subtask_status(
    session: Session, subtask_id: int, is_done: bool
) -> Optional[Subtask]:
    """Перемикання галочки виконано/не виконано для підзадачі"""
    db_subtask = session.get(Subtask, subtask_id)
    if not db_subtask:
        return None

    db_subtask.is_done = is_done
    session.add(db_subtask)

    # Також тригеримо оновлення батьківської задачі
    db_task = session.get(Task, db_subtask.task_id)
    if db_task:
        db_task.updated_at = datetime.now(timezone.utc)
        session.add(db_task)

    session.commit()
    session.refresh(db_subtask)
    return db_subtask
