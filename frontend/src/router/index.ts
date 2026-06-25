import { createRouter, createWebHistory } from "vue-router";
import BoardView from "@/views/BoardView.vue";
import HomeView from "@/views/HomeView.vue";

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: "/",
      name: "home",
      component: HomeView,
    },
    {
      path: "/project/:id", // <--- Динамічний URL з ID проекту
      name: "board",
      component: BoardView,
      props: true, // Дозволяє отримувати :id як звичайний пропс у компоненті
    },
  ],
});

export default router;
