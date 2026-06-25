import { fileURLToPath, URL } from "node:url";
import vue from "@vitejs/plugin-vue";
import { defineConfig, loadEnv } from "vite";

export default defineConfig(({ mode }) => {
  // Зчитуємо змінні з .env файлу папки frontend
  const env = loadEnv(mode, process.cwd(), "");

  const port = Number(env.VITE_PORT) || 5173;
  const backendUrl = env.VITE_BACKEND_URL || "http://127.0.0.1:8000";

  return {
    plugins: [vue()],
    resolve: {
      alias: {
        // Зручний аліас @ для швидких імпортів із папки src/
        "@": fileURLToPath(new URL("./src", import.meta.url)),
      },
    },
    server: {
      port: port,
      strictPort: true,
      host: "127.0.0.1",
      // Налаштування проксі, яке повністю вирішує проблеми мережі у WSL2
      proxy: {
        "/api": {
          target: backendUrl,
          changeOrigin: true,
          secure: false,
        },
      },
    },
  };
});
