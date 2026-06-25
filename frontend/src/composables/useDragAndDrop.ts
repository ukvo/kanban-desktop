import { ref } from "vue";

export function useDragAndDrop(
  onCardDropped: (taskId: number, targetStatusId: number) => Promise<void>,
) {
  // Зберігаємо ID задачі, яку зараз перетягує користувач
  const draggedTaskId = ref<number | null>(null);
  // Зберігаємо ID колонки, над якою зараз зависла картка (для підсвічування стилями)
  const activeDropzoneStatusId = ref<number | null>(null);

  // 1. Початок перетягування картки
  const handleDragStart = (event: DragEvent, taskId: number) => {
    draggedTaskId.value = taskId;
    if (event.dataTransfer) {
      event.dataTransfer.effectAllowed = "move";
      // Передаємо ID як текст для надійності HTML5 API
      event.dataTransfer.setData("text/plain", taskId.toString());
    }
  };

  // 2. Картка зависла над колонкою (обов'язково preventDefault, щоб дозволити drop)
  const handleDragOver = (event: DragEvent, statusId: number) => {
    event.preventDefault();
    activeDropzoneStatusId.value = statusId;
  };

  // 3. Картка покинула межі колонки
  const handleDragLeave = () => {
    activeDropzoneStatusId.value = null;
  };

  // 4. Фінальне скидання картки в нову колонку
  const handleDrop = async (event: DragEvent, targetStatusId: number) => {
    event.preventDefault();
    activeDropzoneStatusId.value = null;

    const taskIdStr =
      event.dataTransfer?.getData("text/plain") ||
      draggedTaskId.value?.toString();
    if (!taskIdStr) return;

    const taskId = Number(taskIdStr);
    draggedTaskId.value = null;

    // Викликаємо зовнішню функцію оновлення даних в базі
    await onCardDropped(taskId, targetStatusId);
  };

  return {
    activeDropzoneStatusId,
    handleDragStart,
    handleDragOver,
    handleDragLeave,
    handleDrop,
  };
}
