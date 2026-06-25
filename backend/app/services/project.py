from typing import Optional, Sequence

from loguru import logger
from sqlmodel import Session, select

from app.models.models import Project


def create_project(session: Session, name: str, description: Optional[str] = None) -> Project:
    """Створення нового проекту/дошки"""
    logger.info(f"Створення проекту: {name}")
    db_project = Project(name=name, description=description)
    session.add(db_project)
    session.commit()
    session.refresh(db_project)
    return db_project


def get_projects(session: Session, skip: int = 0, limit: int = 100) -> Sequence[Project]:
    """Отримання списку всіх проектів"""
    statement = select(Project).offset(skip).limit(limit)
    return session.exec(statement).all()


def get_project_by_id(session: Session, project_id: int) -> Optional[Project]:
    """Пошук конкретного проекту за ID"""
    return session.get(Project, project_id)


def delete_project(session: Session, project_id: int) -> bool:
    """Видалення проекту за ID (із каскадним видаленням задач завдяки конфігу моделі)"""
    db_project = session.get(Project, project_id)
    if not db_project:
        logger.warning(f"Спроба видалити неіснуючий проект з ID: {project_id}")
        return False

    logger.info(f"Видалення проекту з ID: {project_id} ({db_project.name})")
    session.delete(db_project)
    session.commit()
    return True
