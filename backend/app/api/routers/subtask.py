from typing import Optional
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from sqlmodel import Session

from app.core.db import get_session
from app.services import subtask as subtask_service

router = APIRouter(prefix="/subtasks", tags=["Subtasks"])


class SubtaskCreate(BaseModel):
    task_id: int
    text: str
    due_date: Optional[datetime] = None


@router.post("/", status_code=status.HTTP_201_CREATED)
def create_new_subtask(subtask_data: SubtaskCreate, session: Session = Depends(get_session)):
    """Додавання пункту чек-ліста до задачі"""
    subtask = subtask_service.create_subtask(
        session=session,
        task_id=subtask_data.task_id,
        text=subtask_data.text,
        due_date=subtask_data.due_date,
    )
    if not subtask:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Батьківську задачу не знайдено"
        )
    return subtask


@router.patch("/{subtask_id}/toggle")
def toggle_subtask(subtask_id: int, is_done: bool, session: Session = Depends(get_session)):
    """Перемикання статусу виконання підзадачі (виконано / ні)"""
    subtask = subtask_service.toggle_subtask_status(
        session=session, subtask_id=subtask_id, is_done=is_done
    )
    if not subtask:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Підзадачу не знайдено"
        )
    return subtask
