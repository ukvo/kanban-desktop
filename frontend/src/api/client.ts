// Отримуємо значення префіксу з .env файлу Vite
const API_PREFIX = import.meta.env.VITE_API_PREFIX || "/api/v1";

/**
 * Універсальна обгортка над fetch, яка автоматично додає префікс /api/v1
 * @param endpoint Шлях до ендпоінту, наприклад 'projects/' або 'tasks/'
 * @param options Стандартні опції запиту RequestInit
 */
export async function apiFetch<T>(
  endpoint: string,
  options?: RequestInit,
): Promise<T> {
  // Автоматично прибираємо зайвий слеш на початку, якщо користувач його випадково написав
  const cleanEndpoint = endpoint.startsWith("/") ? endpoint.slice(1) : endpoint;
  const url = `${API_PREFIX}/${cleanEndpoint}`;

  const response = await fetch(url, options);
  if (!response.ok) {
    throw new Error(`Помилка запиту до API: ${response.statusText}`);
  }
  return response.json();
}
