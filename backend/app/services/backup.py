from datetime import datetime, timezone
import os
from pathlib import Path
import shutil
import tempfile
import zipfile
from loguru import logger
from app.core.config import settings

BACKUP_DIR = Path("local_backups")


class BackupService:
    """Сервіс для повного автономного керування локальними бекапами бази даних."""

    @staticmethod
    def create_database_backup() -> str:
        """Створює .zip архів бази у папці local_backups."""
        db_url = settings.DATABASE_URL
        if not db_url.startswith("sqlite:///"):
            raise ValueError("Підтримується тільки SQLite.")

        db_filename = db_url.replace("sqlite:///", "")
        db_path = Path(db_filename).absolute()

        if not db_path.exists():
            raise FileNotFoundError(f"Файл бази {db_filename} відсутній.")

        current_time = datetime.now(timezone.utc).strftime("%Y_%m_%d_%H%M%S")
        zip_filename = f"backup_{current_time}.zip"

        BACKUP_DIR.mkdir(exist_ok=True)
        final_zip_path = BACKUP_DIR / zip_filename

        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            temp_db_copy = temp_path / db_path.name

            shutil.copy2(db_path, temp_db_copy)

            with zipfile.ZipFile(final_zip_path, "w", zipfile.ZIP_DEFLATED) as zipf:
                zipf.write(temp_db_copy, arcname=db_path.name)

        logger.success(f"Локальний бекап створено: {final_zip_path.name}")
        return zip_filename

    @staticmethod
    def get_all_backups() -> list:
        """Повертає список усіх бекапів, відсортованих: НАЙНОВІШИЙ ЗВЕРХУ."""
        if not BACKUP_DIR.exists():
            return []

        backups = []
        for file in BACKUP_DIR.glob("backup_*.zip"):
            stat = file.stat()
            backups.append(
                {"filename": file.name, "size_bytes": stat.st_size, "created_at": datetime.fromtimestamp(stat.st_mtime, tz=timezone.utc).isoformat()}
            )

        # Сортуємо за іменем (в імені є дата) у зворотньому порядку -> найновіші зверху
        backups.sort(key=lambda x: x["filename"], reverse=True)
        return backups

    @staticmethod
    def restore_from_backup(filename: str) -> bool:
        """Відновлює базу даних із обраного файлу архіву."""
        from app.core.db import engine

        zip_path = BACKUP_DIR / filename
        if not zip_path.exists():
            return False

        db_url = settings.DATABASE_URL
        db_filename = db_url.replace("sqlite:///", "")
        db_path = Path(db_filename).absolute()

        engine.dispose()

        with zipfile.ZipFile(zip_path, "r") as zipf:
            zipf.extract(db_path.name, path=db_path.parent)

        logger.success(f"Базу успішно відновлено з архіву: {filename}")
        return True

    @staticmethod
    def delete_backup(filename: str) -> bool:
        """Видаляє файл бекапу з диска."""
        zip_path = BACKUP_DIR / filename
        if zip_path.exists():
            os.remove(zip_path)
            logger.info(f"Файл бекапу видалено: {filename}")
            return True
        return False
