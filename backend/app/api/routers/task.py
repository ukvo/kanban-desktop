from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from sqlmodel import Session

from app.core.db import get_session
from app.services import task as task_service

router = APIRouter(prefix="/tasks", tags=["Tasks"])


class TaskCreate(BaseModel):
    project_id: int
    status_id: int
    title: str
    description: Optional[str] = None
    priority: int = 2


class TaskUpdate(BaseModel):
    status_id: Optional[int] = None
    priority: Optional[int] = None


@router.post("/", status_code=status.HTTP_201_CREATED)
def create_new_task(task_data: TaskCreate, session: Session = Depends(get_session)):
    """Створення нової картки задачі"""
    return task_service.create_task(
        session=session,
        project_id=task_data.project_id,
        status_id=task_data.status_id,
        title=task_data.title,
        description=task_data.description,
        priority=task_data.priority,
    )


@router.get("/project/{project_id}")
def read_project_tasks(
    project_id: int, status_id: Optional[int] = None, session: Session = Depends(get_session)
):
    """Отримання всіх задач проекту з автоматичним сортуванням (Kanban-дошка)"""
    return task_service.get_tasks_by_project(
        session=session, project_id=project_id, status_id=status_id
    )


@router.patch("/{task_id}")
def update_task(
    task_id: int, update_data: TaskUpdate, session: Session = Depends(get_session)
):
    """Оновлення колонки або пріоритету (наприклад, при Drag & Drop перетягуванні)"""
    updated_task = task_service.update_task_status_or_priority(
        session=session,
        task_id=task_id,
        status_id=update_data.status_id,
        priority=update_data.priority,
    )
    if not updated_task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Задачу не знайдено")
    return updated_task
