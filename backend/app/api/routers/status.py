from typing import List, Optional
from fastapi import APIRouter, Depends, status
from pydantic import BaseModel
from sqlmodel import Session

from app.core.db import get_session
from app.services import status as status_service

router = APIRouter(prefix="/statuses", tags=["Statuses"])


class StatusCreate(BaseModel):
    name: str
    group: str = "active"


class PositionUpdate(BaseModel):
    status_ids: List[int]


@router.post("/", response_model=None, status_code=status.HTTP_201_CREATED)
def create_new_status(
    status_data: StatusCreate, session: Session = Depends(get_session)
):
    """Ендпоінт для створення нової власної колонки"""
    return status_service.create_status(
        session=session, name=status_data.name, group=status_data.group
    )


@router.get("/", response_model=None)
def read_statuses(group: Optional[str] = None, session: Session = Depends(get_session)):
    """Ендпоінт для отримання списку колонок дошки з автосортуванням"""
    return status_service.get_statuses(session=session, group=group)


@router.post("/reorder", status_code=status.HTTP_200_OK)
def reorder_statuses(
    position_data: PositionUpdate, session: Session = Depends(get_session)
):
    """Ендпоінт для збереження нового порядку колонок після перетягування (Drag & Drop)"""
    status_service.update_status_positions(
        session=session, status_ids=position_data.status_ids
    )
    return {"message": "Порядок колонок успішно оновлено"}
