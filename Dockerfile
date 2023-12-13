FROM python:3.8

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app

COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

COPY . /app/

# RUN python manage.py migrate
# RUN python create_superuser.py
# CMD gunicorn --bind 0.0.0.0:8000 wallet_project.wsgi:application