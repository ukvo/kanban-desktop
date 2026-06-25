### Запуск бакенду  
```bash
uv run uvicorn main:app --reload
```

###### Перевірка та виправлення лінтером
```bash
# Перевірка всього
uv run ruff check

# Автоматичне виправлення
uv run ruff check --fix
```

#### Alembic  

```bash
uv add alembic
```

###### Перша автоматична міграція
```bash
uv run alembic revision --autogenerate -m "initial_migration"
```

###### Застосування міграцій
```bash
uv run alembic upgrade head
```

##### Додавання сервісів гугл  

```bash
uv add google-auth-oauthlib google-api-python-client
```

### Frontend  

```bash
cd ~/kanban-desktop/frontend
bun create vite . --template vue-ts
bun add -d @biomejs/biome sass
bunx @biomejs/biome init
```

###### Перевірка  
```bash
bunx @biomejs/biome check --write .
```

##### Автоматичне виправлення  
```bash
bunx @biomejs/biome migrate --write
```

```bash
bun add vue-router@4
```


---  

### Дізнатися пізніше  

🗄️ Чи потрібно розділяти models на різні файли?  
Для нашого поточного етапу (Варіант №2) розділяти файл models.py на окремі файли (project.py, task.py, status.py) поки що немає гострої потреби, і ось чому:
- **Коли розділення доцільне**: Коли кількість моделей перевищує 7-10 штук, або коли одна модель містить сотні рядків коду бізнес-валідації (Pydantic-методи @field_validator). Також розділення потрібне, якщо моделі використовуються в абсолютно різних ізольованих модулях (наприклад, окремо модуль білінгу, окремо пул задач).  
- **Чому зараз краще тримати в одному файлі**: У SQLModel/SQLAlchemy існує проблема циклічних імпортів (Circular Imports). Оскільки наші таблиці Project, Status, Task та Subtask міцно зв'язані між собою через Foreign Keys та relationship, якщо рознести їх у різні файли, вони почнуть імпортувати один одного по колу. Це призведе до помилки Python при старті сервера. Тримання їх в одному файлі models.py гарантує, що база даних ініціалізується стабільно і без сюрпризів.Тому пропоную залишити їх в єдиному файлі app/models/models.py, просто логічно розділивши коментарями.  
