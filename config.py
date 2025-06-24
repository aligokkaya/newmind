# config.py
import os
from dotenv import load_dotenv

load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), '.env'))


KAFKA_BROKER = os.getenv("KAFKA_BROKER",'localhost:29092')
RAW_TOPIC = os.getenv("RAW_TOPIC")
PROCESSED_TOPIC = os.getenv("PROCESSED_TOPIC")

REDIS_HOST = os.getenv("REDIS_HOST")
REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))

POSTGRES_CONN = {
    "dbname": os.getenv("POSTGRES_DB"),
    "user": os.getenv("POSTGRES_USER"),
    "password": os.getenv("POSTGRES_PASSWORD"),
    "host": os.getenv("POSTGRES_HOST"),
    "port": int(os.getenv("POSTGRES_PORT")),
}

GRPC_HOST = os.getenv("GRPC_HOST")
GRPC_PORT = os.getenv("GRPC_PORT")