import { onMounted, ref } from "vue";

export type Theme = "light" | "dark";

export function useTheme() {
  // Реактивна змінна для поточної теми
  const theme = ref<Theme>("light");

  // Функція для примусового встановлення теми
  const setTheme = (newTheme: Theme) => {
    theme.value = newTheme;
    // Записуємо вибір у LocalStorage
    localStorage.setItem("kanban-theme", newTheme);
    // Вішаємо атрибут на html для SCSS палітр
    document.documentElement.setAttribute("data-theme", newTheme);
  };

  // Функція для перемикання теми (кнопкою в інтерфейсі)
  const toggleTheme = () => {
    setTheme(theme.value === "light" ? "dark" : "light");
  };

  // Ініціалізація теми при монтуванні додатка
  onMounted(() => {
    const savedTheme = localStorage.getItem("kanban-theme") as Theme | null;

    if (savedTheme === "light" || savedTheme === "dark") {
      setTheme(savedTheme);
    } else {
      // Якщо збереженої теми немає — зчитуємо системні налаштування ОС Windows/WSL
      const systemPrefersDark = window.matchMedia(
        "(prefers-color-scheme: dark)",
      ).matches;
      setTheme(systemPrefersDark ? "dark" : "light");
    }
  });

  return {
    theme,
    toggleTheme,
    setTheme,
  };
}
