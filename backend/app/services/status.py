from typing import List, Optional, Sequence

from loguru import logger
from sqlmodel import Session, func, select, col

from app.models.models import Status


def create_status(session: Session, name: str, group: str = "active") -> Status:
    """Створення нового статусу (колонки) з автоматичним призначенням позиції"""
    # Визначаємо максимальну поточну позицію колонок, щоб поставити нову в кінець
    max_position = session.exec(select(func.max(Status.position))).one()
    next_position = (max_position or 0) + 1 if max_position is not None else 0

    logger.info(f"Створення стовпця '{name}' на позиції {next_position}")
    db_status = Status(name=name, group=group, position=next_position)
    session.add(db_status)
    session.commit()
    session.refresh(db_status)
    return db_status


def get_statuses(session: Session, group: Optional[str] = None) -> Sequence[Status]:
    """Отримання списку колонок, відсортованих зліва направо за полем position"""
    statement = select(Status)
    if group:
        statement = statement.where(Status.group == group)

    # Сортуємо колонки за позицією, щоб фронтенд отримував їх у правильному порядку
    statement = statement.order_by(col(Status.position))
    return session.exec(statement).all()


def update_status_positions(session: Session, status_ids: List[int]) -> bool:
    """Оновлення порядку колонок на дошці (використовується при Drag&Drop колонок)"""
    logger.info("Оновлення черговості позицій колонок")
    for index, status_id in enumerate(status_ids):
        db_status = session.get(Status, status_id)
        if db_status:
            db_status.position = index
            session.add(db_status)
    session.commit()
    return True
