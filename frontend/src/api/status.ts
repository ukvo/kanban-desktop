import { apiFetch } from "./client";

export interface Status {
  id: number;
  name: string;
  group: string;
  position: number;
}

/**
 * Отримання списку всіх активних колонок (статусів) дошки
 */
export async function fetchStatuses(): Promise<Status[]> {
  return apiFetch<Status[]>("statuses/");
}
