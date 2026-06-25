<script setup lang="ts">
import { onMounted, ref } from "vue";
import {
  fetchSyncStatus,
  restoreFromCloud,
  type SyncStatusResponse,
  triggerCloudBackup,
} from "@/api/backup";

const syncData = ref<SyncStatusResponse | null>(null);
const isProcessing = ref(false);
const errorMessage = ref<string | null>(null);

// 1. Завантаження поточного статусу синхронізації з бекенду
const loadSyncStatus = async () => {
  try {
    errorMessage.value = null;
    syncData.value = await fetchSyncStatus();
  } catch (error) {
    errorMessage.value = "Не вдалося отримати статус хмари";
  }
};

// 2. Обробник кнопки «Завантажити в хмару»
const handleUpload = async () => {
  try {
    isProcessing.value = true;
    await triggerCloudBackup();
    await loadSyncStatus(); // Перевіряємо статус заново
  } catch (error) {
    alert("Помилка завантаження бекапу");
  } finally {
    isProcessing.value = false;
  }
};

// 3. Обробник кнопки «Оновити з хмари»
const handleDownload = async () => {
  if (!syncData.value?.drive_id) return;
  if (
    !confirm(
      "Ви впевнені? Поточна локальна база буде повністю замінена версією з хмари!",
    )
  )
    return;

  try {
    isProcessing.value = true;
    await restoreFromCloud(syncData.value.drive_id);
    window.location.reload(); // Перезавантажуємо сторінку для оновлення всіх дошок
  } catch (error) {
    alert("Помилка відновлення бази з хмари");
  } finally {
    isProcessing.value = false;
  }
};

onMounted(() => {
  loadSyncStatus();
});
</script>

<template>
  <div class="sync-widget" :class="syncData?.status?.toLowerCase() || 'loading'">
    <div class="widget-info">
      <!-- Кольоровий статус-маркер -->
      <span class="status-indicator"></span>
      <div class="status-text">
        <span class="status-title">{{ syncData?.message || 'Перевірка хмари...' }}</span>
        <small v-if="syncData?.cloud_backup_at" class="status-date">
          Хмара від: {{ new Date(syncData.cloud_backup_at).toLocaleString() }}
        </small>
      </div>
    </div>

    <!-- Кнопки керування залежно від статусу -->
    <div v-if="syncData && !isProcessing" class="widget-actions">
      <button 
        v-if="syncData.status === 'NEED_UPLOAD' || syncData.status === 'SYNCED'" 
        class="btn-sync upload"
        @click="handleUpload"
      >
        ☁️ Завантажити в хмару
      </button>
      
      <button 
        v-if="syncData.status === 'NEED_DOWNLOAD'" 
        class="btn-sync download"
        @click="handleDownload"
      >
        📥 Оновити з хмари
      </button>
    </div>

    <div v-else-if="isProcessing" class="widget-loading">Обробка...</div>
    <div v-if="errorMessage" class="widget-error">{{ errorMessage }}</div>
  </div>
</template>

<style lang="scss" scoped>
.sync-widget {
  display: flex;
  justify-content: space-between;
  align-items: center;
  background-color: var(--bg-surface);
  border: 1px solid var(--border-color);
  border-radius: 8px;
  padding: 12px 16px;
  margin-bottom: 24px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.01);

  // Кольорові стилі для різних станів хмари
  &.synced .status-indicator { background-color: #28a745; }
  &.need_upload .status-indicator { background-color: #ffc107; }
  &.need_download .status-indicator { background-color: #007bff; }
  &.loading .status-indicator { background-color: var(--text-muted); }
}

.widget-info {
  display: flex;
  align-items: center;
  gap: 12px;
}

.status-indicator {
  width: 10px;
  height: 10px;
  border-radius: 50%;
  display: inline-block;
  flex-shrink: 0;
}

.status-text {
  display: flex;
  flex-direction: column;
}

.status-title {
  font-size: 14px;
  font-weight: 500;
  color: var(--text-primary);
}

.status-date {
  font-size: 11px;
  color: var(--text-muted);
  margin-top: 2px;
}

.btn-sync {
  border: 1px solid transparent;
  padding: 6px 12px;
  border-radius: 6px;
  font-size: 12px;
  font-weight: 500;
  cursor: pointer;
  transition: filter 0.2s;

  &:hover {
    filter: brightness(0.9);
  }

  &.upload {
    background-color: var(--text-primary);
    color: var(--bg-main);
  }

  &.download {
    background-color: #007bff;
    color: white;
  }
}

.widget-loading, .widget-error {
  font-size: 13px;
  color: var(--text-muted);
}

.widget-error {
  color: #dc3545;
}
</style>
