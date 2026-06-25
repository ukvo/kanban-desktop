import { apiFetch } from "./client";

export interface SyncStatusResponse {
  status: "SYNCED" | "NEED_UPLOAD" | "NEED_DOWNLOAD";
  message: string;
  local_updated_at: string;
  cloud_backup_at: string | null;
  drive_id?: string;
}

/**
 * Отримання поточного статусу актуальності бази даних (Локальна vs Хмара)
 */
export async function fetchSyncStatus(): Promise<SyncStatusResponse> {
  return apiFetch<SyncStatusResponse>("backup/status");
}

/**
 * Створення локального бекапу та його автоматичне завантаження в хмару
 */
export async function triggerCloudBackup(): Promise<{
  status: string;
  message: string;
}> {
  return apiFetch<{ status: string; message: string }>("backup/create", {
    method: "POST",
  });
}

/**
 * Скачування бекапу з хмари та повне відновлення локальної бази SQLite
 */
export async function restoreFromCloud(
  driveId: string,
): Promise<{ status: string; message: string }> {
  return apiFetch<{ status: string; message: string }>("backup/restore", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ drive_id: driveId }),
  });
}
