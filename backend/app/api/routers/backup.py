from fastapi import APIRouter, Depends, status, HTTPException
from pydantic import BaseModel
from app.services.backup import BackupService
from app.services.google_drive import GoogleDriveService
from app.services.sync import SyncService
from app.core.db import get_session
from sqlmodel import Session

router = APIRouter(prefix="/backup", tags=["Backup"])


@router.post("/create", status_code=status.HTTP_200_OK)
def trigger_backup():
    """Ендпоінт для створення локального бекапу та його автоматичного завантаження в хмару."""
    try:
        # 1. Незалежно створюємо локальний .zip архів у temp_backups/
        zip_path = BackupService.create_database_backup()

        # 2. Незалежно ініціалізуємо сервіс Диску та заливаємо готовий файл у хмару
        drive_service = GoogleDriveService()
        drive_file_id = drive_service.upload_file_to_backup_folder(zip_path)

        return {
            "status": "success",
            "message": "Резервну копію бази даних успішно створено та завантажено на Google Диск",
            "local_path": zip_path,
            "google_drive_file_id": drive_file_id,
        }
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Не вдалося виконати синхронізацію: {str(e)}")


@router.get("/status", status_code=status.HTTP_200_OK)
def get_sync_status(session: Session = Depends(get_session)):
    """Ендпоінт для перевірки статусу актуальності бази даних (локальна vs хмара)."""
    try:
        status_info = SyncService.check_sync_status(session)
        return status_info
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Не вдалося перевірити статус синхронізації: {str(e)}")


class RestoreRequest(BaseModel):
    drive_id: str


@router.post("/restore", status_code=status.HTTP_200_OK)
def restore_from_cloud(restore_data: RestoreRequest):
    """Ендпоінт для скачування бекапу з хмари та повного оновлення локальної бази даних."""
    import os

    try:
        # 1. Створюємо шлях для тимчасового скачування архіву
        temp_zip_path = os.path.abspath("temp_backups/cloud_download.zip")

        # 2. Скачуємо файл через Google Drive Service
        drive_service = GoogleDriveService()
        drive_service.download_file_from_drive(restore_data.drive_id, temp_zip_path)

        # 3. Відновлюємо базу за допомогою BackupService
        success = BackupService.restore_database_from_zip(temp_zip_path)

        # Видаляємо тимчасовий завантажений zip-файл, щоб не накопичувати сміття
        if os.path.exists(temp_zip_path):
            os.remove(temp_zip_path)

        if not success:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Файл архіву виявився пошкодженим або не містить файлу бази даних.")

        return {"status": "success", "message": "Локальну базу даних успішно оновлено до версії з хмари"}

    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Не вдалося виконати відновлення з хмари: {str(e)}")
