from datetime import datetime, timezone
from sqlmodel import Session, select, func
from app.models.models import Task
from app.services.google_drive import GoogleDriveService


class SyncService:
    """Сервіс порівняння актуальності даних між локальною базою та хмарою."""

    @staticmethod
    def check_sync_status(session: Session) -> dict:
        """Порівнює мітки часу локальних змін та хмарного бекапу."""
        # 1. Отримуємо час останньої зміни в локальній базі задач
        # Використовуємо col(Task.updated_at) для сумісності з Pylance
        from sqlmodel import col

        max_local_time = session.exec(select(func.max(col(Task.updated_at)))).one()

        # Якщо в базі взагалі немає задач, ставимо дефолтну стару дату
        local_timestamp = max_local_time if max_local_time else datetime.fromtimestamp(0, tz=timezone.utc)

        # 2. Отримуємо інфо про останній бекап з Google Диску
        drive_service = GoogleDriveService()
        cloud_backup = drive_service.get_latest_backup_info()

        # Якщо в хмарі взагалі немає бекапів
        if not cloud_backup:
            return {
                "status": "NEED_UPLOAD",
                "message": "У хмарі немає бекапів. Локальну базу потрібно завантажити.",
                "local_updated_at": local_timestamp.isoformat(),
                "cloud_backup_at": None,
            }

        # Конвертуємо ISO-час створення файлу з Google API у об'єкт datetime Python
        # Замінюємо 'Z' на '+00:00' для правильного парсингу таймзони
        cloud_time_str = cloud_backup["cloud_created_at"].replace("Z", "+00:00")
        cloud_timestamp = datetime.fromisoformat(cloud_time_str)

        # 3. ПОРІВНЯННЯ
        # Даємо невеликий зазор у 5 секунд на мережеві затримки
        time_difference = (local_timestamp - cloud_timestamp).total_seconds()

        if time_difference > 5:
            return {
                "status": "NEED_UPLOAD",
                "message": "Локальні дані новіші. Рекомендовано завантажити бекап у хмару.",
                "local_updated_at": local_timestamp.isoformat(),
                "cloud_backup_at": cloud_timestamp.isoformat(),
            }
        elif time_difference < -5:
            return {
                "status": "NEED_DOWNLOAD",
                "message": "У хмарі є свіжіші дані. Рекомендовано оновити локальну базу.",
                "local_updated_at": local_timestamp.isoformat(),
                "cloud_backup_at": cloud_timestamp.isoformat(),
                "drive_id": cloud_backup["drive_id"],
            }
        else:
            return {
                "status": "SYNCED",
                "message": "Дані повністю синхронізовані.",
                "local_updated_at": local_timestamp.isoformat(),
                "cloud_backup_at": cloud_timestamp.isoformat(),
            }
