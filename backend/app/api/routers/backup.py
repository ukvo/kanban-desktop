import os
from fastapi import APIRouter, HTTPException, status, File, UploadFile
from fastapi.responses import FileResponse
from pydantic import BaseModel
from app.services.backup import BackupService, BACKUP_DIR

router = APIRouter(prefix="/backup", tags=["Local Backup Manager"])


class BackupActionRequest(BaseModel):
    filename: str


@router.post("/create", status_code=status.HTTP_201_CREATED)
def create_backup():
    """Створення нового локального бекапу."""
    try:
        filename = BackupService.create_database_backup()
        return {"status": "success", "filename": filename}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/list", response_model=None)
def list_backups():
    """Отримання списку всіх бекапів (найновіший зверху)."""
    return BackupService.get_all_backups()


@router.get("/download/{filename}")
def download_backup_file(filename: str):
    """Ендпоінт для фізичного скачування файлу бекапу у браузер."""
    file_path = BACKUP_DIR / filename
    if not file_path.exists():
        raise HTTPException(status_code=404, detail="Файл бекапу не знайдено")
    return FileResponse(path=file_path, filename=filename, media_type="application/zip")


@router.post("/restore", status_code=status.HTTP_200_OK)
def restore_backup(data: BackupActionRequest):
    """Відновлення локальної бази даних з обраного архіву."""
    success = BackupService.restore_from_backup(data.filename)
    if not success:
        raise HTTPException(status_code=404, detail="Не вдалося відновити базу")
    return {"status": "success", "message": "Базу даних успішно відновлено"}


@router.delete("/delete/{filename}", status_code=status.HTTP_200_OK)
def delete_backup_file(filename: str):
    """Видалення файлу бекапу."""
    success = BackupService.delete_backup(filename)
    if not success:
        raise HTTPException(status_code=404, detail="Файл не знайдено")
    return {"status": "success", "message": "Файл успішно видалено"}


@router.post("/upload", status_code=status.HTTP_201_CREATED)
async def upload_backup_file(file: UploadFile = File(...)):
    """Ендпоінт для завантаження готового .zip файлу бекапу з комп'ютера користувача."""
    # Перевіряємо, чи це дійсно ZIP-архів
    if not file.filename or not file.filename.endswith(".zip"):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Дозволено завантажувати тільки файли з розширенням .zip")

    # Створюємо папку, якщо її немає
    BACKUP_DIR.mkdir(exist_ok=True)

    # Формуємо безпечний шлях для збереження файлу на диску
    file_path = BACKUP_DIR / file.filename

    try:
        # Асинхронно записуємо байти файлу на диск
        with open(file_path, "wb") as buffer:
            content = await file.read()
            buffer.write(content)

        return {"status": "success", "message": f"Файл {file.filename} успішно завантажено в локальне сховище бекапів"}
    except Exception as e:
        if file_path.exists():
            os.remove(file_path)
        raise HTTPException(status_code=500, detail=f"Не вдалося зберегти файл: {str(e)}")
