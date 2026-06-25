<script setup lang="ts">
import { onMounted, ref } from "vue";
import { createProject, fetchProjects, type Project } from "@/api/project";
import ProjectModal from "@/components/ProjectModal.vue";

const projects = ref<Project[]>([]);
const isLoading = ref(true);
const errorMessage = ref<string | null>(null);

// Стан відкриття модального вікна
const isModalOpen = ref(false);

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

// Функція обробки створення нової дошки з форми модалки
const handleCreateProject = async (data: {
  name: string;
  description: string;
}) => {
  try {
    const newProject = await createProject(data.name, data.description);
    // Реактивно додаємо новий проект на початок списку без перезавантаження сторінки
    projects.value.unshift(newProject);
  } catch (error) {
    alert(error instanceof Error ? error.message : "Не вдалося створити дошку");
  }
};

onMounted(() => {
  loadProjects();
});
</script>

<template>
  <section class="projects-section">

    <div class="section-header">
      <h2>Ваші Kanban-дошки</h2>
      <button class="btn-create" @click="isModalOpen = true">+ Створити дошку</button>
    </div>

    <div v-if="isLoading" class="info-message">Завантаження дошок з бази даних...</div>
    <div v-else-if="errorMessage" class="error-message">{{ errorMessage }}</div>

    <div v-else-if="projects.length > 0" class="projects-grid">
      <RouterLink 
        v-for="project in projects" 
        :key="project.id" 
        :to="{ name: 'board', params: { id: project.id } }" 
        class="project-card"
      >
        <h3>{{ project.name }}</h3>
        <p>{{ project.description || 'Немає опису' }}</p>
        <span class="project-date">Створено: {{ new Date(project.created_at).toLocaleDateString() }}</span>
      </RouterLink>
    </div>

    <div v-else class="info-message">У вас поки немає створених дошок.</div>

    <!-- Підключаємо наш компонент модалки -->
    <ProjectModal 
      :is-open="isModalOpen" 
      @close="isModalOpen = false" 
      @submit="handleCreateProject"
    />
  </section>
</template>

<style lang="scss" scoped>
.projects-section {
  margin-top: 32px;
}

.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 24px;

  h2 {
    font-size: 20px;
    margin: 0;
    color: var(--text-primary);
  }
}

.btn-create {
  background-color: var(--text-primary);
  color: var(--bg-main);
  border: 1px solid transparent;
  padding: 10px 16px;
  border-radius: 6px;
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
  transition: filter 0.2s;

  &:hover {
    filter: brightness(0.9);
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
  text-decoration: none;

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
