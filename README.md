# Глоссарий API

API сервис для управления глоссарием терминов, построенный с использованием FastAPI. Позволяет создавать, читать, обновлять и удалять термины через REST API.

## Возможности

- ✨ Получение списка всех терминов с пагинацией
- 🔍 Поиск термина по ключевому слову
- ➕ Добавление новых терминов
- 📝 Обновление существующих терминов
- ❌ Удаление терминов из глоссария
- 📚 Автоматическая документация API (Swagger UI и ReDoc)
- 🔄 Автоматические миграции базы данных

## Технологии

- [FastAPI](https://fastapi.tiangolo.com/) - современный веб-фреймворк
- [SQLAlchemy](https://www.sqlalchemy.org/) - SQL тулкит и ORM
- [Pydantic](https://pydantic-docs.helpmanual.io/) - валидация данных
- [SQLite](https://www.sqlite.org/) - база данных
- [Alembic](https://alembic.sqlalchemy.org/) - миграции базы данных
- [Docker](https://www.docker.com/) - контейнеризация

## Установка и запуск

### Через Docker (рекомендуется)

1. Убедитесь, что у вас установлен Docker и Docker Compose

2. Клонируйте репозиторий:

```bash
git clone https://github.com/your-repo/glossary-api.git
cd glossary-api
```

3. Запустите сервис:

```bash
docker compose up -d
```

Приложение будет доступно по адресу: `http://localhost:8000`

### Локальная установка

1. Клонируйте репозиторий:

```bash
git clone https://github.com/your-repo/glossary-api.git
cd glossary-api
```

2. Создайте и активируйте виртуальное окружение:

```bash
python -m venv venv
source venv/bin/activate
```

3. Установите зависимости:

```bash
pip install -r requirements.txt
```

4. Запустите сервис:

```bash
uvicorn src.main:app --reload
```

## Использование API

### Документация API

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc
- OpenAPI JSON: http://localhost:8000/openapi.json

### Примеры запросов

#### Получение всех терминов

```bash
curl http://localhost:8000/terms/
```

#### Получение конкретного термина

```bash
curl http://localhost:8000/terms/{название_термина}
```

#### Добавление нового термина

```bash
curl -X POST http://localhost:8000/terms/ \
-H "Content-Type: application/json" \
-d '{"term": "Docker", "description": "Платформа для контейнеризации приложений"}'
```

#### Обновление термина

```bash
curl -X PUT http://localhost:8000/terms/docker \
-H "Content-Type: application/json" \
-d '{"description": "Обновленное описание Docker"}'
```

#### Удаление термина

```bash
curl -X DELETE http://localhost:8000/terms/python
```

## Работа с базой данных

### Просмотр данных

1. Через Python-скрипт:

```bash
python check_db.py
```
2. Через SQLite CLI в контейнере:

```bash
docker-compose exec web sh
sqlite3 /app/data/glossary.db
```

## Разработка

### Создание новой миграции

После изменения моделей данных создайте новую миграцию:

```bash
alembic revision --autogenerate -m "Описание изменений"
```

### Применение миграций

Миграции применяются автоматически при запуске приложения, но их можно применить вручную:

```bash
alembic upgrade head
```