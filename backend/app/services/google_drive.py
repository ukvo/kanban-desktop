from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from loguru import logger

from app.services.google_auth import get_google_credentials


class GoogleDriveService:
    """Сервіс для безпосередньої взаємодії з Google Drive API."""

    def __init__(self):
        # 1. Автоматично підтягуємо наші валідні OAuth2 токени
        creds = get_google_credentials()
        # 2. Ініціалізуємо офіційний клієнт Google Drive v3
        self.service = build("drive", "v3", credentials=creds)

    def get_or_create_app_folder(self) -> str:
        """
        Шукає папку 'kanban' в корені Google Диску додатка.
        Якщо папки немає — створює її та повертає унікальний Drive ID.
        """
        folder_name = "kanban"

        # Формуємо рядок запиту для пошуку папки (тільки тип folder і назва kanban)
        query = f"name = '{folder_name}' and mimeType = 'application/vnd.google-apps.folder' and trashed = false"

        try:
            # Шукаємо папку на Диску
            response = self.service.files().list(q=query, spaces="drive", fields="files(id, name)").execute()

            files = response.get("files", [])

            # Якщо папка знайдена — повертаємо її унікальний ID
            if files:
                folder_id = files[0]["id"]
                logger.info(f"Знайдено існуючу папку '{folder_name}' на Google Диску з ID: {folder_id}")
                return folder_id

            # Якщо папки немає — створюємо її в корені Диску
            folder_metadata = {"name": folder_name, "mimeType": "application/vnd.google-apps.folder"}

            folder = self.service.files().create(body=folder_metadata, fields="id").execute()

            new_folder_id = folder.get("id")
            logger.success(f"На Google Диску успішно створено нову папку '{folder_name}' з ID: {new_folder_id}")
            return new_folder_id

        except Exception as e:
            logger.error(f"Помилка при роботі з папками на Google Диску: {str(e)}")
            raise e

    def get_or_create_subfolder(self, parent_id: str, subfolder_name: str) -> str:
        """Шукає або створює підпапку всередині батьківської папки kanban."""
        query = f"name = '{subfolder_name}' and '{parent_id}' in parents and mimeType = 'application/vnd.google-apps.folder' and trashed = false"
        try:
            response = self.service.files().list(q=query, spaces="drive", fields="files(id, name)").execute()
            files = response.get("files", [])

            if files:
                return files[0]["id"]

            # Якщо підпапки немає — створюємо її з прив'язкою до батьківського ID
            folder_metadata = {"name": subfolder_name, "mimeType": "application/vnd.google-apps.folder", "parents": [parent_id]}
            folder = self.service.files().create(body=folder_metadata, fields="id").execute()
            return folder.get("id")
        except Exception as e:
            logger.error(f"Помилка створення підпапки {subfolder_name}: {str(e)}")
            raise e

    def upload_file_to_backup_folder(self, local_file_path: str, mime_type: str = "application/zip") -> str:
        """
        Повністю автоматичний процес: знаходить головну папку,
        створює підпапку бекапів та завантажує туди локальний файл.
        """
        import os

        # 1. Отримуємо ланцюжок папок у хмарі
        main_folder_id = self.get_or_create_app_folder()
        backup_folder_id = self.get_or_create_subfolder(main_folder_id, "database_backup")

        file_name = os.path.basename(local_file_path)
        logger.info(f"Запуск завантаження файлу {file_name} на Google Диск...")

        # 2. Налаштовуємо метадані файлу в хмарі (вказуємо назву та батьківську папку)
        file_metadata = {"name": file_name, "parents": [backup_folder_id]}

        # 3. Готуємо файл до передачі через медіа-потік Google API
        media = MediaFileUpload(local_file_path, mimetype=mime_type, resumable=True)

        try:
            uploaded_file = self.service.files().create(body=file_metadata, media_body=media, fields="id").execute()

            drive_id = uploaded_file.get("id")
            logger.success(f"Файл {file_name} успішно завантажено на Google Диск з ID: {drive_id}")
            return drive_id
        except Exception as e:
            logger.error(f"Помилка завантаження файлу на Google Диск: {str(e)}")
            raise e
