FROM python:3.10.12-slim

WORKDIR /app

COPY . .

RUN pip install --no-cache-dir --upgrade pip && \
    pip install -r /app/library_management/requirements.txt

ENV PYTHONUNBUFFERED=1
ENV DJANGO_SETTINGS_MODULE=library_management.settings

EXPOSE ${BACKEND_PORT}

WORKDIR /app/library_management
