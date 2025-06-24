import time
import random
import uuid
from kafka import KafkaProducer
import json
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from config import KAFKA_BROKER, RAW_TOPIC 

COMMENTS = [
    "Servis çok hızlıydı.",
    "Yemekler çok lezzetliydi.",
    "Garsonlar biraz ilgisizdi.",
    "Ambiyans çok hoştu.",
    "Porsiyonlar küçüktü ama lezzetliydi.",
    "Fiyatlar biraz pahalı.",
    "Yine geleceğim!",
    "Tatlılar harikaydı.",
    "Kahve soğuktu.",
    "Beklediğim kadar iyi değildi.",
    "Restoran çok kalabalıktı.",
    "Mekan ferah ve temizdi.",
    "Kapanış saati çok erken.",
    "Hizmet kalitesi mükemmeldi.",
    "Rezervasyon almıyorlar.",
    "Menü çok çeşitliydi.",
    "Et yemeği çok sertti.",
    "Tatlılar aşırı şekerliydi.",
    "Garsonlar çok ilgiliydi.",
    "Yemekler çok yavaştı."
]
print(KAFKA_BROKER)
producer = KafkaProducer(
    bootstrap_servers=KAFKA_BROKER,
    value_serializer=lambda v: json.dumps(v).encode("utf-8")
)

def generate_comment():
    comment_text = random.choice(COMMENTS)
    comment = {
        "commentId": str(uuid.uuid4()),
        "text": comment_text,
        "timestamp": time.time()
    }
    return comment


while True:
    comment = generate_comment()
    print(f"Producing: {comment}")
    producer.send(RAW_TOPIC, comment)
    producer.flush()
    time.sleep(random.uniform(0.2, 5))  # rastgele üretim aralığı