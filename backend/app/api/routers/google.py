from fastapi import APIRouter, status
from app.services.google_drive import GoogleDriveService

router = APIRouter(prefix="/google", tags=["Google Auth"])


@router.post("/login", status_code=status.HTTP_200_OK)
def google_login_test():
    """Ендпоінт для первинного запуску авторизації Google через браузер."""
    from app.services.google_auth import get_google_credentials
    get_google_credentials()
    return {"message": "Авторизація успішно пройдена, токен збережено"}


@router.post("/init-folder", status_code=status.HTTP_200_OK)
def google_folder_init_test():
    """Ендпоінт для перевірки створення кореневої папки 'kanban' на Google Диску."""
    # Ініціалізуємо сервіс Диску
    drive_service = GoogleDriveService()
    # Запускаємо створення папки
    folder_id = drive_service.get_or_create_app_folder()
    return {
        "message": "Перевірка папки пройшла успішно",
        "google_drive_folder_id": folder_id
    }
