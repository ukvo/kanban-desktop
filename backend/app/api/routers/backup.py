from fastapi import APIRouter, status, HTTPException
from app.services.backup import BackupService
from app.services.google_drive import GoogleDriveService

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
