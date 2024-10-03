FROM python:3.12

WORKDIR /backend

# Сначала копируем файл зависимостей
COPY ./requirements/dev.txt /backend/requirements/dev.txt

# Устанавливаем зависимости
RUN pip install --no-cache-dir requests
RUN pip install --no-cache-dir --upgrade pip setuptools
RUN pip install --no-cache-dir -r /backend/requirements/dev.txt

# Устанавливаем PostgreSQL клиент для проверки состояния базы данных
RUN apt-get update && apt-get install -y postgresql-client

# Копируем .env файл (если он существует)
COPY .env /backend/.env

# Копируем все файлы проекта в контейнер
COPY . /backend

# Запускаем сервер Django с ожиданием PostgreSQL
CMD ["sh", "-c", "until pg_isready -h $PG_HOST -p $PG_PORT -U $PG_USER; do echo waiting for postgres; sleep 2; done && python manage.py migrate && python manage.py collectstatic --noinput && gunicorn --bind 0.0.0.0:8000 main.wsgi:application"]

EXPOSE 8000

