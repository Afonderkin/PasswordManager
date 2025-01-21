# Используем официальный образ Python
FROM python:3.11-slim

# Устанавливаем рабочую директорию
WORKDIR /app

# Копируем только requirements.txt для оптимизации кэширования
COPY requirements.txt .

# Устанавливаем зависимости
RUN pip install --no-cache-dir -r requirements.txt

# Копируем весь проект
COPY . .

# Указываем переменные окружения
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Указываем рабочую директорию для Django
WORKDIR /app/password_manager

# Команда для запуска сервера
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]