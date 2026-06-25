<script setup lang="ts">
import { computed, onMounted, ref } from "vue";
import { RouterLink, useRoute } from "vue-router";
import { fetchStatuses, type Status } from "@/api/status";
import {
  fetchPriorityLabels,
  fetchTasksByProject,
  type Task,
} from "@/api/task";

const route = useRoute();
const projectId = Number(route.params.id);

const columns = ref<Status[]>([]);
const tasks = ref<Task[]>([]);
const isLoading = ref(true);
const errorMessage = ref<string | null>(null);

// Мапа текстових назв для рівнів пріоритету
const priorityLabels = ref<Record<number, string>>({});

// Функція паралельного завантаження колонок та задач
const loadBoardData = async () => {
  try {
    isLoading.value = true;
    errorMessage.value = null;

    // 3. Додаємо третій паралельний запит у Promise.all
    const [statusesResponse, tasksResponse, prioritiesResponse] =
      await Promise.all([
        fetchStatuses(),
        fetchTasksByProject(projectId),
        fetchPriorityLabels(), // <--- Скачуємо довідник з бекенду
      ]);

    columns.value = statusesResponse;
    tasks.value = tasksResponse;
    priorityLabels.value = prioritiesResponse; // <--- Записуємо дані з бази
  } catch (error) {
    errorMessage.value =
      error instanceof Error ? error.message : "Не вдалося завантажити дошку";
  } finally {
    isLoading.value = false;
  }
};

/**
 * Важлива логіка: групуємо задачі за ID колонки (status_id).
 * Vue автоматично перераховує цей розподіл при будь-якій зміні масиву задач.
 */
const tasksByColumn = computed(() => {
  const grouped: Record<number, Task[]> = {};

  // Ініціалізуємо порожні масиви для кожної існуючої колонки
  for (const col of columns.value) {
    grouped[col.id] = [];
  }

  // Розподіляємо задачі за їхнім статусом
  for (const task of tasks.value) {
    if (grouped[task.status_id]) {
      grouped[task.status_id].push(task);
    }
  }

  return grouped;
});

onMounted(() => {
  loadBoardData();
});
</script>

<template>
  <div class="board-page">
    <nav class="board-nav">
      <RouterLink to="/" class="back-link">&larr; Назад до всіх дошок</RouterLink>
    </nav>

    <div v-if="isLoading" class="info-message">Завантаження даних дошки...</div>
    <div v-else-if="errorMessage" class="error-message">{{ errorMessage }}</div>

    <div v-else class="kanban-board">
      <div v-for="column in columns" :key="column.id" class="kanban-column">
        <header class="column-header">
          <h3>{{ column.name }}</h3>
          <!-- Динамічно рахуємо кількість задач у цій колонці -->
          <span class="task-count">{{ tasksByColumn[column.id]?.length || 0 }}</span>
        </header>

        <div class="column-body">
          <!-- Рендеримо картки задач, якщо вони є в цій колонці -->
          <template v-if="tasksByColumn[column.id] && tasksByColumn[column.id].length > 0">
            <div 
              v-for="task in tasksByColumn[column.id]" 
              :key="task.id" 
              class="kanban-card"
              :class="`priority-${task.priority}`"
            >
              <h4>{{ task.title }}</h4>
              <p v-if="task.description">{{ task.description }}</p>
              
              <footer class="card-footer">
                <span class="priority-badge">{{ priorityLabels[task.priority] }}</span>
              </footer>
            </div>
          </template>
          
          <!-- Якщо задач в колонці немає -->
          <div v-else class="empty-column-text">Немає задач</div>
        </div>
      </div>
    </div>
  </div>
</template>

<style lang="scss" scoped>
@use "@/assets/styles/variables";

.board-page {
  margin-top: 24px;
}

.board-nav {
  margin-bottom: 24px;

  .back-link {
    color: var(--text-muted);
    text-decoration: none;
    font-size: 14px;
    font-weight: 500;
    transition: color 0.2s;

    &:hover {
      color: var(--text-primary);
    }
  }
}

.kanban-board {
  display: flex;
  gap: 20px;
  align-items: flex-start;
  overflow-x: auto;
  padding-bottom: 16px;
  min-height: calc(100vh - 180px);
}

.kanban-column {
  background-color: var(--bg-surface);
  border: 1px solid var(--border-color);
  border-radius: variables.$column-radius;
  width: 320px;
  min-width: 320px;
  max-height: calc(100vh - 200px);
  display: flex;
  flex-direction: column;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.01);
}

.column-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 16px;
  border-bottom: 1px solid var(--border-color);

  h3 {
    margin: 0;
    font-size: 16px;
    font-weight: 600;
    color: var(--text-primary);
  }

  .task-count {
    background-color: var(--bg-main);
    color: var(--text-muted);
    font-size: 12px;
    font-weight: 600;
    padding: 2px 8px;
    border-radius: 20px;
    border: 1px solid var(--border-color);
  }
}

.column-body {
  padding: 16px;
  flex-grow: 1;
  overflow-y: auto;
  display: flex;
  flex-direction: column;
  gap: 12px;
  min-height: 150px;
}

.kanban-card {
  background-color: var(--bg-main);
  border: 1px solid var(--border-color);
  border-radius: variables.$card-radius;
  padding: 12px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.01);
  border-left: 4px solid var(--border-color); // Дефолтна ліва рамка
  transition: transform 0.2s, box-shadow 0.2s;
  cursor: pointer;

  &:hover {
    transform: translateY(-2px);
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.04);
  }

  h4 {
    margin: 0 0 6px 0;
    font-size: 14px;
    font-weight: 600;
    color: var(--text-primary);
  }

  p {
    margin: 0 0 12px 0;
    font-size: 13px;
    color: var(--text-muted);
    line-height: 1.4;
    display: -webkit-box;
    -webkit-line-clamp: 2; // Обрізає опис до двох рядків на дошці
    -webkit-box-orient: vertical;
    overflow: hidden;
  }
}

// Динамічне фарбування лівої рамки карти залежно від її пріоритету з CSS-змінних
.kanban-card.priority-1 { border-left-color: var(--priority-low); }
.kanban-card.priority-2 { border-left-color: var(--priority-medium); }
.kanban-card.priority-3 { border-left-color: var(--priority-high); }

.card-footer {
  display: flex;
  justify-content: flex-end;
}

.priority-badge {
  font-size: 11px;
  font-weight: 500;
  color: var(--text-muted);
  background-color: var(--bg-surface);
  border: 1px solid var(--border-color);
  padding: 2px 6px;
  border-radius: 4px;
}

.empty-column-text {
  color: var(--text-muted);
  text-align: center;
  font-size: 13px;
  padding: 20px 0;
  border: 1px dashed var(--border-color);
  border-radius: variables.$card-radius;
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
