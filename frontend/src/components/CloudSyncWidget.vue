<script setup lang="ts">
import { onMounted, ref } from "vue";
import {
  createLocalBackup,
  deleteBackupFile,
  fetchBackupsList,
  getBackupDownloadUrl,
  type LocalBackup,
  restoreFromBackup,
  uploadBackupFile,
} from "@/api/backup";

const backups = ref<LocalBackup[]>([]);
const isProcessing = ref(false);
const fileInput = ref<HTMLInputElement | null>(null);

// 1. Отримання актуального списку копій
const loadBackups = async () => {
  try {
    backups.value = await fetchBackupsList();
  } catch (error) {
    console.error("Не вдалося завантажити список бекапів");
  }
};

// 2. Створення нового бекапу кнопки
const handleCreateBackup = async () => {
  try {
    isProcessing.value = true;
    await createLocalBackup();
    await loadBackups();
  } catch (error) {
    alert("Помилка створення резервної копії");
  } finally {
    isProcessing.value = false;
  }
};

// 3. Відновлення бази з обраного файлу
const handleRestore = async (filename: string) => {
  if (
    !confirm(
      `Ви впевнені? Поточна база даних буде повністю замінена архівом: ${filename}`,
    )
  )
    return;
  try {
    isProcessing.value = true;
    await restoreFromBackup(filename);
    window.location.reload(); // Перезавантажуємо сторінку для відображення відновлених дошок
  } catch (error) {
    alert("Помилка відновлення даних");
  } finally {
    isProcessing.value = false;
  }
};

// 4. Видалення архіву з диска
const handleDelete = async (filename: string) => {
  if (!confirm(`Видалити файл бекапу ${filename}?`)) return;
  try {
    await deleteBackupFile(filename);
    await loadBackups();
  } catch (error) {
    alert("Не вдалося видалити файл");
  }
};

// 5. Функція обробки завантаження файлу з комп'ютера (Міграція)
const handleFileUpload = async (event: Event) => {
  const target = event.target as HTMLInputElement;
  const file = target.files?.[0];
  if (!file) return;

  try {
    isProcessing.value = true;
    await uploadBackupFile(file);
    await loadBackups(); // Оновлюємо список
    alert("Файл успішно імпортовано в систему бекапів!");
  } catch (error) {
    alert(
      error instanceof Error ? error.message : "Помилка завантаження файлу",
    );
  } finally {
    isProcessing.value = false;
    if (fileInput.value) fileInput.value.value = ""; // Очищаємо інпут
  }
};

// Допоміжна функція переведення байтів у мегабайти
const formatSize = (bytes: number) => {
  return `${(bytes / (1024 * 1024)).toFixed(2)} MB`;
};

onMounted(() => {
  loadBackups();
});
</script>

<template>
  <div class="backup-manager-box">
    <header class="manager-header">
      <div class="header-title-block">
        <h3>📦 Локальний менеджер копій</h3>
        <small class="offline-badge">Offline-First</small>
      </div>
      
      <div class="header-actions">
        <!-- Прихований нативний інпут для вибору файлу з ПК -->
        <input 
          ref="fileInput"
          type="file" 
          accept=".zip" 
          style="display: none" 
          @change="handleFileUpload"
        />
        <button class="btn-action upload-pc" :disabled="isProcessing" @click="fileInput?.click()">
          📥 Імпортувати .zip з ПК
        </button>
        <button class="btn-action create" :disabled="isProcessing" @click="handleCreateBackup">
          ➕ Створити копію бази
        </button>
      </div>
    </header>

    <!-- Відображення списку створених архівів -->
    <div v-if="backups.length > 0" class="backups-list-wrapper">
      <table class="backups-table">
        <thead>
          <tr>
            <th>Назва файлу архіву</th>
            <th>Розмір</th>
            <th>Дата створення</th>
            <th class="actions-col">Дії</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="backup in backups" :key="backup.filename">
            <td class="filename-cell"><code>{{ backup.filename }}</code></td>
            <td>{{ formatSize(backup.size_bytes) }}</td>
            <td>{{ new Date(backup.created_at).toLocaleString() }}</td>
            <td class="actions-cell">
              <!-- Пряме посилання на скачування файлу у браузер Windows -->
              <a :href="getBackupDownloadUrl(backup.filename)" class="action-link download" title="Скачати на ПК">
                💾 Скачати
              </a>
              <button class="action-btn restore" @click="handleRestore(backup.filename)" title="Відновити базу з цього файлу">
                🔄 Відновити
              </button>
              <button class="action-btn delete" @click="handleDelete(backup.filename)" title="Видалити архів">
                ❌
              </button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <div v-else class="empty-backups-text">
      У вас поки немає збережених резервних копій бази даних.
    </div>
  </div>
</template>

<style lang="scss" scoped>
.backup-manager-box {
  background-color: var(--bg-surface);
  border: 1px solid var(--border-color);
  border-radius: 12px;
  padding: 20px;
  margin-bottom: 32px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.02);
}

.manager-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 16px;
  padding-bottom: 14px;
  border-bottom: 1px solid var(--border-color);
}

.header-title-block {
  display: flex;
  align-items: center;
  gap: 12px;

  h3 {
    margin: 0;
    font-size: 16px;
    font-weight: 600;
  }
}

.offline-badge {
  background-color: rgba(40, 167, 69, 0.1);
  color: #28a745;
  font-size: 11px;
  font-weight: 600;
  padding: 2px 8px;
  border-radius: 20px;
  border: 1px solid rgba(40, 167, 69, 0.2);
}

.header-actions {
  display: flex;
  gap: 12px;
}

.btn-action {
  padding: 8px 14px;
  border-radius: 6px;
  font-size: 13px;
  font-weight: 500;
  cursor: pointer;
  border: 1px solid transparent;
  transition: filter 0.2s;

  &:hover:not(:disabled) {
    filter: brightness(0.9);
  }

  &:disabled {
    opacity: 0.5;
    cursor: not-allowed;
  }

  &.create {
    background-color: var(--text-primary);
    color: var(--bg-main);
  }

  &.upload-pc {
    background-color: transparent;
    border-color: var(--border-color);
    color: var(--text-primary);

    &:hover {
      background-color: var(--bg-main);
    }
  }
}

.backups-list-wrapper {
  max-height: 200px;
  overflow-y: auto;
  border: 1px solid var(--border-color);
  border-radius: 8px;
}

.backups-table {
  width: 100%;
  border-collapse: collapse;
  font-size: 13px;
  text-align: left;

  th, td {
    padding: 10px 12px;
    border-bottom: 1px solid var(--border-color);
  }

  th {
    background-color: var(--bg-main);
    color: var(--text-muted);
    font-weight: 500;
    position: sticky;
    top: 0;
    z-index: 10;
  }

  tr:last-child td {
    border-bottom: none;
  }
}

.filename-cell code {
  background-color: var(--bg-main);
  padding: 2px 6px;
  border-radius: 4px;
  font-family: monospace;
  color: var(--text-primary);
}

.actions-col {
  text-align: right;
}

.actions-cell {
  display: flex;
  justify-content: flex-end;
  align-items: center;
  gap: 14px;
}

.action-link {
  color: #007bff;
  text-decoration: none;
  font-weight: 500;
  
  &:hover {
    text-decoration: underline;
  }
}

.action-btn {
  background: none;
  border: none;
  font-size: 13px;
  font-weight: 500;
  cursor: pointer;
  padding: 0;

  &.restore {
    color: #28a745;
    &:hover { text-decoration: underline; }
  }

  &.delete {
    opacity: 0.6;
    &:hover { opacity: 1; }
  }
}

.empty-backups-text {
  text-align: center;
  color: var(--text-muted);
  font-size: 13px;
  padding: 24px 0;
}
</style>
