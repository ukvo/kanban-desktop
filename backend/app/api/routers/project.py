from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from sqlmodel import Session

from app.core.db import get_session
from app.services import project as project_service

router = APIRouter(prefix="/projects", tags=["Projects"])


# Створюємо Pydantic-схему для валідації вхідних даних від фронтенду
class ProjectCreate(BaseModel):
    name: str
    description: Optional[str] = None


@router.post("/", response_model=None, status_code=status.HTTP_201_CREATED)
def create_new_project(
    project_data: ProjectCreate, session: Session = Depends(get_session)
):
    """Ендпоінт для створення нової Kanban-дошки (проекту)"""
    return project_service.create_project(
        session=session,
        name=project_data.name,
        description=project_data.description,
    )


@router.get("/", response_model=None)
def read_projects(
    skip: int = 0, limit: int = 100, session: Session = Depends(get_session)
):
    """Ендпоінт для отримання списку всіх проектів"""
    return project_service.get_projects(session=session, skip=skip, limit=limit)


@router.delete("/{project_id}", status_code=status.HTTP_204_NO_CONTENT)
def remove_project(project_id: int, session: Session = Depends(get_session)):
    """Ендпоінт для видалення проекту за його ID"""
    success = project_service.delete_project(session=session, project_id=project_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Проект з ID {project_id} не знайдено",
        )
