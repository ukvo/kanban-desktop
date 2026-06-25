from fastapi import APIRouter, status, HTTPException
from app.services.backup import BackupService

router = APIRouter(prefix="/backup", tags=["Backup"])


@router.post("/create", status_code=status.HTTP_200_OK)
def trigger_backup():
    """Ендпоінт для створення ручного локального бекапу бази даних."""
    try:
        # Викликаємо наш ізольований сервіс
        zip_path = BackupService.create_database_backup()

        # Для тесту повертаємо інформацію про створений файл
        return {"message": "Резервну копію бази даних успішно створено локально", "archive_path": zip_path}
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Не вдалося створити резервну копію: {str(e)}")
