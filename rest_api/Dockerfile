FROM python:3.10-slim

WORKDIR /app

# Ortak config dosyaları
COPY config.py .
COPY .env .
COPY requirements.txt .

# Uygulama kodları
COPY rest_api/ .

RUN pip install --no-cache-dir fastapi uvicorn sqlalchemy psycopg2-binary python-dotenv

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]