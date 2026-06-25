<script setup lang="ts">
import { onMounted, ref } from "vue";
import { fetchProjects, type Project } from "@/api/project";
import { useTheme } from "@/composables/useTheme";

// 1. Активуємо сервіс тем
const { theme, toggleTheme } = useTheme();

// 2. Створюємо реактивний масив для збереження проектів з бази даних
const projects = ref<Project[]>([]);
const isLoading = ref(true);
const errorMessage = ref<string | null>(null);

// 3. Функція завантаження дошок через наш API-клієнт
const loadProjects = async () => {
  try {
    isLoading.value = true;
    errorMessage.value = null;
    projects.value = await fetchProjects();
  } catch (error) {
    errorMessage.value =
      error instanceof Error ? error.message : "Сталася невідома помилка";
  } finally {
    isLoading.value = false;
  }
};

// 4. Тригеримо завантаження при першому відкритті додатку
onMounted(() => {
  loadProjects();
});
</script>

<template>
  <main class="app-container">
    <header class="app-header">
      <h1>Персональна Kanban Дошка</h1>
      
      <button class="theme-toggle-btn" @click="toggleTheme">
        Режим: {{ theme === 'light' ? '☀️ Світлий' : '🌙 Темний' }}
      </button>
    </header>

    <!-- Секція відображення проектів -->
    <section class="projects-section">
      <h2>Ваші Kanban-дошки</h2>

      <!-- Індикатор завантаження -->
      <div v-if="isLoading" class="info-message">Завантаження дошок з бази даних...</div>

      <!-- Повідомлення про помилку -->
      <div v-else-if="errorMessage" class="error-message">{{ errorMessage }}</div>

      <!-- Список проектів -->
      <div v-else-if="projects.length > 0" class="projects-grid">
        <div v-for="project in projects" :key="project.id" class="project-card">
          <h3>{{ project.name }}</h3>
          <p>{{ project.description || 'Немає опису' }}</p>
          <span class="project-date">Створено: {{ new Date(project.created_at).toLocaleDateString() }}</span>
        </div>
      </div>

      <!-- Повідомлення, якщо дошок ще немає -->
      <div v-else class="info-message">У вас поки немає створених дошок.</div>
    </section>
  </main>
</template>

<style lang="scss" scoped>
.app-container {
  min-height: 100vh;
  padding: 24px;
}

.app-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding-bottom: 16px;
  border-bottom: 1px solid var(--border-color);

  h1 {
    font-size: 24px;
    margin: 0;
  }
}

.theme-toggle-btn {
  background-color: var(--bg-surface);
  color: var(--text-primary);
  border: 1px solid var(--border-color);
  padding: 8px 16px;
  border-radius: 6px;
  cursor: pointer;
  font-weight: 500;
  font-size: 14px;
  transition: background-color 0.2s, border-color 0.2s;

  &:hover {
    filter: brightness(0.9);
  }
}

.projects-section {
  margin-top: 32px;

  h2 {
    font-size: 20px;
    margin-bottom: 20px;
    color: var(--text-primary);
  }
}

.projects-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 20px;
}

.project-card {
  background-color: var(--bg-surface);
  border: 1px solid var(--border-color);
  border-radius: 8px;
  padding: 16px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.02);
  transition: transform 0.2s, box-shadow 0.2s;

  &:hover {
    transform: translateY(-2px);
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
  }

  h3 {
    margin: 0 0 8px 0;
    font-size: 18px;
    color: var(--text-primary);
  }

  p {
    margin: 0 0 16px 0;
    font-size: 14px;
    color: var(--text-muted);
    line-height: 1.4;
  }
}

.project-date {
  font-size: 12px;
  color: var(--text-muted);
  display: block;
}

.info-message {
  color: var(--text-muted);
  text-align: center;
  padding: 40px;
}

.error-message {
  color: var(--priority-high);
  background-color: rgba(220, 53, 69, 0.1);
  padding: 12px;
  border-radius: 6px;
  text-align: center;
}
</style>
