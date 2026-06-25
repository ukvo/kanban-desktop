<script setup lang="ts">
import { onMounted, ref } from "vue";
import { RouterLink, useRoute } from "vue-router";
import { fetchStatuses, type Status } from "@/api/status";

const route = useRoute();
// Отримуємо ID проекту з URL-маршруту
const projectId = route.params.id;

const columns = ref<Status[]>([]);
const isLoading = ref(true);
const errorMessage = ref<string | null>(null);

const loadBoardData = async () => {
  try {
    isLoading.value = true;
    errorMessage.value = null;

    // Завантажуємо активні колонки для дошки
    columns.value = await fetchStatuses();
  } catch (error) {
    errorMessage.value =
      error instanceof Error ? error.message : "Не вдалося завантажити дошку";
  } finally {
    isLoading.value = false;
  }
};

onMounted(() => {
  loadBoardData();
});
</script>

<template>
  <div class="board-page">
    <!-- Навігація назад на головну сторінку -->
    <nav class="board-nav">
      <RouterLink to="/" class="back-link">&larr; Назад до всіх дошок</RouterLink>
    </nav>

    <div v-if="isLoading" class="info-message">Завантаження колонок Kanban...</div>
    <div v-else-if="errorMessage" class="error-message">{{ errorMessage }}</div>

    <!-- Горизонтальний ряд Kanban-колонок -->
    <div v-else class="kanban-board">
      <div v-for="column in columns" :key="column.id" class="kanban-column">
        <header class="column-header">
          <h3>{{ column.name }}</h3>
          <span class="task-count">0</span>
        </header>

        <!-- Сюди в майбутньому будуть падати картки задач -->
        <div class="column-body">
          <div class="empty-column-text">Немає задач</div>
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

.empty-column-text {
  color: var(--text-muted);
  text-align: center;
  font-size: 14px;
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
