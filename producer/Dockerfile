FROM python:3.10-slim

WORKDIR /app

# producer kodları
COPY producer/producer.py .

# Ortak config dosyaları
COPY config.py .
COPY .env .

COPY requirements.txt .

RUN pip install kafka-python grpcio redis psycopg2-binary python-dotenv

CMD ["python", "producer.py"]