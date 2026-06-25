import os
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from loguru import logger

# Область доступу: повне керування файлами у Google Диску користувача
SCOPES = ["https://www.googleapis.com/auth/drive.file"]


def get_google_credentials() -> Credentials:
    """Отримує або оновлює токени доступу Google OAuth2."""
    creds = None
    token_path = "token.json"
    creds_path = "credentials.json"

    # 1. Перевіряємо, чи користувач уже авторизувався раніше (файл token.json)
    if os.path.exists(token_path):
        creds = Credentials.from_authorized_user_file(token_path, SCOPES)

    # 2. Якщо токена немає або він застарів — оновлюємо або створюємо його
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            logger.info("Оновлення застарілого токена Google...")
            creds.refresh(Request())
        else:
            if not os.path.exists(creds_path):
                logger.error(f"Файл {creds_path} відсутній у папці backend!")
                raise FileNotFoundError(f"Файл {creds_path} не знайдено.")

            logger.info("Запуск первинної авторизації через браузер...")
            flow = InstalledAppFlow.from_client_secrets_file(creds_path, SCOPES)
            # Запускаємо локальний сервер для отримання коду авторизації
            creds = flow.run_local_server(port=0)

        # 3. Зберігаємо отриманий токен на майбутнє
        with open(token_path, "w") as token_file:
            token_file.write(creds.to_json())
            logger.success("Токен Google успішно збережено в token.json")

    return creds # type: ignore
