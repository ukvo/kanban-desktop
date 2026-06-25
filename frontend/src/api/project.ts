import { apiFetch } from "./client";

export interface Project {
  id: number;
  name: string;
  description: string | null;
  created_at: string;
}

/**
 * Отримання списку всіх проектів/дошок за допомогою нашого клієнта
 */
export async function fetchProjects(): Promise<Project[]> {
  return apiFetch<Project[]>("projects/");
}

/**
 * Створення нової Kanban-дошки (проекту)
 */
export async function createProject(
  name: string,
  description?: string,
): Promise<Project> {
  return apiFetch<Project>("projects/", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ name, description }),
  });
}
