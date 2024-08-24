FROM python:3.12

WORKDIR /app

COPY ./requirements/dev.txt /app

RUN pip install --no-cache-dir --upgrade pip setuptools
RUN pip install --no-cache-dir -r dev.txt

# Установите PostgreSQL клиент для доступа к pg_isready
RUN apt-get update && apt-get install -y postgresql-client

COPY .env .env

COPY . /app

CMD ["sh", "-c", "until pg_isready -h $PG_HOST -p $PG_PORT -U $PG_USER; do echo waiting for postgres; sleep 2; done && python manage.py migrate && python manage.py collectstatic --noinput && gunicorn --bind 0.0.0.0:8000 main.wsgi:application"]

EXPOSE 8000

