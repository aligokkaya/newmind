import json
import time
import grpc
import redis
import psycopg2
from kafka import KafkaConsumer, KafkaProducer
from datetime import datetime
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'grpc_service')))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from sentiment_pb2 import SentimentRequest
from sentiment_pb2_grpc import SentimentAnalyzerStub
from config import (
    RAW_TOPIC,
    PROCESSED_TOPIC,
    KAFKA_BROKER,
    REDIS_HOST,
    REDIS_PORT,
    POSTGRES_CONN,
    GRPC_HOST,
    GRPC_PORT
)

pg_conn = psycopg2.connect(**POSTGRES_CONN)
pg_cursor = pg_conn.cursor()

def ensure_table_exists():
    pg_cursor.execute("""
        CREATE TABLE IF NOT EXISTS comments (
            comment_id UUID PRIMARY KEY,
            text TEXT NOT NULL,
            sentiment VARCHAR(10) NOT NULL,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
    """)
    pg_conn.commit()

ensure_table_exists()

redis_client = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, decode_responses=True)

channel = grpc.insecure_channel(f"{GRPC_HOST}:{GRPC_PORT}")
grpc_client = SentimentAnalyzerStub(channel)

consumer = KafkaConsumer(
    RAW_TOPIC,
    bootstrap_servers=KAFKA_BROKER,
    value_deserializer=lambda m: json.loads(m.decode("utf-8")),
    auto_offset_reset='earliest',
    enable_auto_commit=True,
    group_id='sentiment-group'
)

producer = KafkaProducer(
    bootstrap_servers=KAFKA_BROKER,
    value_serializer=lambda m: json.dumps(m).encode("utf-8")
)

# === Yardımcı Fonksiyonlar ===

def get_cached_sentiment(text):
    return redis_client.get(text)

def cache_sentiment(text, sentiment, ttl=3600):
    redis_client.setex(text, ttl, sentiment)

def save_to_postgres(comment_id, text, sentiment, timestamp):
    try:
        ts = datetime.fromtimestamp(float(timestamp))
    except Exception:
        ts = datetime.utcnow()
    pg_cursor.execute(
        "INSERT INTO comments (comment_id, text, sentiment, timestamp) VALUES (%s, %s, %s, %s) ON CONFLICT DO NOTHING",
        (comment_id, text, sentiment, ts)
    )
    pg_conn.commit()

def process_comment(message):
    comment_id = message.get("commentId")
    text = message.get("text")
    timestamp = message.get("timestamp")

    sentiment = get_cached_sentiment(text)
    if not sentiment:
        for attempt in range(3):
            try:
                request = SentimentRequest(text=text)
                response = grpc_client.Analyze(request)
                sentiment = response.sentiment
                cache_sentiment(text, sentiment)
                break
            except grpc.RpcError as e:
                print(f"[ERROR] gRPC başarısız: {e.details()}")
                if attempt == 2:
                    return
                time.sleep(1)

    print(f"[Consumer] İşlendi: {text} => {sentiment}")

    result = {
        "commentId": comment_id,
        "text": text,
        "sentiment": sentiment,
        "timestamp": timestamp
    }

    save_to_postgres(comment_id, text, sentiment, timestamp)
    producer.send(PROCESSED_TOPIC, result)

def run():
    print("Consumer başlatıldı. Yorumlar dinleniyor...")
    for msg in consumer:
        process_comment(msg.value)

run()