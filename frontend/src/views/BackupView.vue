<script setup lang="ts">
import { RouterLink } from 'vue-router'
import CloudSyncWidget from '@/components/CloudSyncWidget.vue'
</script>

<template>
  <div class="backup-page">
    <nav class="page-nav">
      <!-- Чітке повернення на головний роут дошок -->
      <RouterLink to="/" class="back-link">&larr; Головна (Назад до дошок)</RouterLink>
    </nav>
    
    <CloudSyncWidget />
  </div>
</template>

<style lang="scss" scoped>
.backup-page {
  margin-top: 24px;
}
.page-nav {
  margin-bottom: 24px;
  .back-link {
    color: var(--text-muted);
    text-decoration: none;
    font-size: 14px;
    font-weight: 500;
    &:hover { color: var(--text-primary); }
  }
}
</style>
