import { apiFetch } from "./client";

// Схема опису локального бекапу
export interface LocalBackup {
  filename: string;
  size_bytes: number;
  created_at: string;
}

/**
 * Отримання списку всіх локальних бекапів (найновіші зверху)
 */
export async function fetchBackupsList(): Promise<LocalBackup[]> {
  return apiFetch<LocalBackup[]>("backup/list");
}

/**
 * Створення нового локального бекапу
 */
export async function createLocalBackup(): Promise<{
  status: string;
  filename: string;
}> {
  return apiFetch<{ status: string; filename: string }>("backup/create", {
    method: "POST",
  });
}

/**
 * Відновлення бази даних із обраного файлу архіву
 */
export async function restoreFromBackup(
  filename: string,
): Promise<{ status: string; message: string }> {
  return apiFetch<{ status: string; message: string }>("backup/restore", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ filename }),
  });
}

/**
 * Видалення файлу бекапу з диска
 */
export async function deleteBackupFile(
  filename: string,
): Promise<{ status: string; message: string }> {
  return apiFetch<{ status: string; message: string }>(
    `backup/delete/${filename}`,
    {
      method: "DELETE",
    },
  );
}

/**
 * Фізичне скачування файлу бекапу у браузер.
 * Оскільки fetch тут не потрібен, ми просто повертаємо пряме URL посилання для завантаження через браузер.
 */
export function getBackupDownloadUrl(filename: string): string {
  const prefix = import.meta.env.VITE_API_PREFIX || "/api/v1";
  return `${prefix}/backup/download/${filename}`;
}

/**
 * Завантаження файлу .zip з комп'ютера на сервер (Міграція/Перенос даних)
 */
export async function uploadBackupFile(
  file: File,
): Promise<{ status: string; message: string }> {
  const prefix = import.meta.env.VITE_API_PREFIX || "/api/v1";
  const formData = new FormData();
  formData.append("file", file);

  const response = await fetch(`${prefix}/backup/upload`, {
    method: "POST",
    body: formData, // FormData автоматично виставить потрібний multipart/form-data заголовок
  });

  if (!response.ok) {
    const errData = await response.json();
    throw new Error(errData.detail || "Не вдалося завантажити файл бекапу");
  }
  return response.json();
}
