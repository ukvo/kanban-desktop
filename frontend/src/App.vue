<script setup lang="ts">
import { RouterView } from "vue-router";
import { useTheme } from "@/composables/useTheme";

const { theme, toggleTheme } = useTheme();
</script>

<template>
  <main class="app-container">
    <header class="app-header">
      <h1>Персональна Kanban Дошка</h1>
      
      <button class="theme-toggle-btn" @click="toggleTheme">
        Режим: {{ theme === 'light' ? '☀️ Світлий' : '🌙 Темний' }}
      </button>
    </header>

    <!-- Тут автоматично рендериться поточна активна сторінка (зараз це HomeView) -->
    <RouterView />
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
</style>
