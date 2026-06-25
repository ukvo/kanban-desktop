import { apiFetch } from "./client";

// Інтерфейс задачі, що повністю відповідає схемі з нашого FastAPI бекенду
export interface Task {
  id: number;
  project_id: number;
  status_id: number;
  title: string;
  description: string | null;
  priority: number; // 1-Low, 2-Medium, 3-High
  created_at: string;
  updated_at: string;
}

/**
 * Отримання списку всіх задач для конкретного проекту (дошки)
 */
export async function fetchTasksByProject(projectId: number): Promise<Task[]> {
  return apiFetch<Task[]>(`tasks/project/${projectId}`);
}

/**
 * Створення нової картки задачі всередині конкретної дошки та колонки
 */
export async function createTask(taskData: {
  project_id: number;
  status_id: number;
  title: string;
  description?: string;
  priority?: number;
}): Promise<Task> {
  return apiFetch<Task>("tasks/", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(taskData),
  });
}

export async function updateTask(
  taskId: number,
  taskData: { status_id?: number; priority?: number },
): Promise<Task> {
  return apiFetch<Task>(`tasks/${taskId}`, {
    method: "PATCH",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(taskData),
  });
}

export async function fetchPriorityLabels(): Promise<Record<number, string>> {
  return apiFetch<Record<number, string>>("tasks/priorities");
}
