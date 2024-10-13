# Используем официальный образ Python
FROM python:3.12

# Устанавливаем необходимые зависимости
WORKDIR /app
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Копируем исходники проекта
COPY . /app

# Команда для запуска Daphne
CMD ["daphne", "-b", "0.0.0.0", "-p", "9000", "main.asgi:application"]