from datetime import datetime, timezone
from pathlib import Path
import shutil
import tempfile
import zipfile
from loguru import logger
from app.core.config import settings


class BackupService:
    """Сервіс для створення локальних резервних копій бази даних."""

    @staticmethod
    def create_database_backup() -> str:
        """
        Бере поточну базу даних з налаштувань, архівує її у .zip
        та повертає повний шлях до згенерованого файлу архіву.
        """
        # 1. Розбираємо URL бази даних, щоб отримати чистий шлях до файлу sqlite
        db_url = settings.DATABASE_URL
        if not db_url.startswith("sqlite:///"):
            logger.error(f"Універсальний бекап файлів підтримує тільки SQLite. Поточний URL: {db_url}")
            raise ValueError("Резервне копіювання файлів підтримується тільки для SQLite баз даних.")

        # Отримуємо ім'я або відносний шлях файлу бази (напр. kanban.db)
        db_filename = db_url.replace("sqlite:///", "")
        db_path = Path(db_filename).absolute()

        if not db_path.exists():
            logger.error(f"Файл бази даних не знайдено за шляхом: {db_path}")
            raise FileNotFoundError(f"Файл бази даних {db_filename} відсутній.")

        # 2. Формуємо назву архіву з міткою часу (Формат: backup_YYYY_MM_DD_HHMM.zip)
        current_time = datetime.now(timezone.utc).strftime("%Y_%m_%d_%H%M")
        zip_filename = f"backup_{current_time}.zip"

        # Створюємо глобальну папку для тимчасових бекапів у проекті, якщо її немає
        backup_dir = Path("temp_backups")
        backup_dir.mkdir(exist_ok=True)
        final_zip_path = backup_dir / zip_filename

        # 3. Створюємо бекап через тимчасову папку ОС (щоб уникнути колізій під час запису в базу)
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            temp_db_copy = temp_path / db_path.name

            # Копіюємо робочу базу даних у тимчасову директорію
            logger.info(f"Копіювання бази даних для архівації: {db_path.name}")
            shutil.copy2(db_path, temp_db_copy)

            # Також перевіряємо та копіюємо тимчасові журнали SQLite, якщо вони активні в цей момент
            wal_file = Path(f"{db_path}-wal")
            shutil_file = Path(f"{db_path}-shm")
            if wal_file.exists():
                shutil.copy2(wal_file, temp_path / wal_file.name)
            if shutil_file.exists():
                shutil.copy2(shutil_file, temp_path / shutil_file.name)

            # 4. Стискаємо файли у .zip архів
            logger.info(f"Архівація бази даних у файл: {final_zip_path}")
            with zipfile.ZipFile(final_zip_path, "w", zipfile.ZIP_DEFLATED) as zipf:
                # Записуємо копію бази в архів під її оригінальним іменем
                zipf.write(temp_db_copy, arcname=db_path.name)

                # Якщо були файли журналів — додаємо і їх
                if wal_file.exists():
                    zipf.write(temp_path / wal_file.name, arcname=wal_file.name)
                if shutil_file.exists():
                    zipf.write(temp_path / shutil_file.name, arcname=shutil_file.name)

        logger.success(f"Резервну копію успішно створено локально за шляхом: {final_zip_path}")
        return str(final_zip_path.absolute())
