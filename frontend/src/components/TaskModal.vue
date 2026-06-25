<script setup lang="ts">
import { ref, watch } from "vue";

const props = defineProps<{
  isOpen: boolean;
  priorities: Record<number, string>;
}>();

const emit = defineEmits<{
  (e: "close"): void;
  (
    e: "submit",
    data: { title: string; description: string; priority: number },
  ): void;
}>();

const title = ref("");
const description = ref("");
const priority = ref(2); // Дефолтний пріоритет — Середній (2)

// Очищуємо поля форми при кожному відкритті модалки
watch(
  () => props.isOpen,
  (newVal) => {
    if (newVal) {
      title.value = "";
      description.value = "";
      priority.value = 2;
    }
  },
);

const handleClose = () => {
  emit("close");
};

const handleSubmit = () => {
  if (!title.value.trim()) return;
  emit("submit", {
    title: title.value.trim(),
    description: description.value.trim(),
    priority: Number(priority.value),
  });
  handleClose();
};
</script>

<template>
  <div v-if="isOpen" class="modal-overlay" @click.self="handleClose">
    <div class="modal-content">
      <header class="modal-header">
        <h2>Створення нової задачі</h2>
        <button class="close-btn" @click="handleClose">&times;</button>
      </header>

      <form @submit.prevent="handleSubmit" class="modal-form">
        <div class="form-group">
          <label for="task-title">Назва задачі *</label>
          <input 
            id="task-title" 
            v-model="title" 
            type="text" 
            placeholder="Наприклад: Написати документацію API" 
            required 
            maxlength="255"
          />
        </div>

        <div class="form-group">
          <label for="task-priority">Пріоритет</label>
          <select id="task-priority" v-model="priority">
            <option 
              v-for="(label, value) in priorities" 
              :key="value" 
              :value="value"
            >
              {{ label }}
            </option>
          </select>
        </div>

        <div class="form-group">
          <label for="task-desc">Опис задачі</label>
          <textarea 
            id="task-desc" 
            v-model="description" 
            placeholder="Детальний опис завдання..." 
            rows="4"
          ></textarea>
        </div>

        <footer class="modal-footer">
          <button type="button" class="btn btn-secondary" @click="handleClose">Скасувати</button>
          <button type="submit" class="btn btn-primary" :disabled="!title.trim()">Додати</button>
        </footer>
      </form>
    </div>
  </div>
</template>

<style lang="scss" scoped>
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
  backdrop-filter: blur(2px);
}

.modal-content {
  background-color: var(--bg-surface);
  border: 1px solid var(--border-color);
  border-radius: 12px;
  width: 100%;
  max-width: 500px;
  box-shadow: 0 10px 25px rgba(0, 0, 0, 0.15);
  overflow: hidden;
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 16px 24px;
  border-bottom: 1px solid var(--border-color);

  h2 {
    margin: 0;
    font-size: 18px;
    color: var(--text-primary);
  }
}

.close-btn {
  background: none;
  border: none;
  font-size: 24px;
  color: var(--text-muted);
  cursor: pointer;
  
  &:hover {
    color: var(--text-primary);
  }
}

.modal-form {
  padding: 24px;
}

.form-group {
  margin-bottom: 20px;

  label {
    display: block;
    font-size: 14px;
    font-weight: 500;
    margin-bottom: 8px;
    color: var(--text-primary);
  }

  input, textarea, select {
    width: 100%;
    padding: 10px 12px;
    border: 1px solid var(--border-color);
    border-radius: 6px;
    background-color: var(--bg-main);
    color: var(--text-primary);
    font-size: 14px;
    box-sizing: border-box;

    &:focus {
      outline: none;
      border-color: var(--text-muted);
    }
  }

  select {
    cursor: pointer;
  }
}

.modal-footer {
  display: flex;
  justify-content: flex-end;
  gap: 12px;
  margin-top: 24px;
}

.btn {
  padding: 10px 16px;
  border-radius: 6px;
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
  border: 1px solid transparent;

  &-secondary {
    background-color: transparent;
    border-color: var(--border-color);
    color: var(--text-primary);

    &:hover {
      background-color: var(--bg-main);
    }
  }

  &-primary {
    background-color: var(--text-primary);
    color: var(--bg-main);

    &:hover:not(:disabled) {
      filter: brightness(0.9);
    }

    &:disabled {
      opacity: 0.5;
      cursor: not-allowed;
    }
  }
}
</style>
