# Указываем базовый образ Python
FROM python:3.12-slim

# Устанавливаем рабочую директорию внутри контейнера
WORKDIR /app

# Устанавливаем зависимости
RUN uv venv

# Копируем все файлы проекта
COPY . .

# Настраиваем переменные окружения для Django
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Открываем порт для Django (по умолчанию 8000)
EXPOSE 8000

# Команда для запуска приложения
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
