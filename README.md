# 📉 Real-Time Sentiment Analysis Pipeline

Bu proje, günlük yorum verilerinin Kafka ile akıtılıp, gRPC ile duygu analizine sokulduğu, Redis ile cache edildiği ve PostgreSQL ile kalıcılaştırıldığı bir mikroservis mimarisi sunar. Kullanıcılar yorumların sonucunu REST API ile sorgulayabilir.

---

## 📆 Mimarideki Servisler

### 1. `producer`

* Kafka'ya yorumları gönderir.
* `config.py` dosyasından `KAFKA_BROKER`, `RAW_TOPIC` değerlerini alır.

#### Komutla başlatma:

```bash
docker exec -it sentiment-producer python producer.py
```

### 2. `consumer`

* Kafka'dan `raw-comments` topic'ini dinler.
* Redis cache kontrolü yapar.
* gRPC ile duygu analizi yapar.
* PostgreSQL'e yazar ve `processed-comments` topic'ine yayar.

#### Ana dosya: `consumer/consumer.py`

### 3. `grpc_service`

* Yorumun pozitif/negatif olup olmadığını belirleyen basit bir servistir.
* `sentiment.proto` ile tanımlı gRPC servisini sunar.

#### Komutla test:

```bash
docker exec -it sentiment-grpc_service python sentiment_service.py
```

### 4. `rest_api`

* Kullanıcılara PostgreSQL'den yorumları döner.
* `FastAPI` üzerinde filtreli sorgu yapılabilir.
* Endpoint:

  * `GET /comments`
  * `GET /comments?sentiment=positive`

### 5. `postgres`

* `comments` tablosunu barındırır:

```sql
CREATE TABLE IF NOT EXISTS comments (
    comment_id UUID PRIMARY KEY,
    text TEXT NOT NULL,
    sentiment VARCHAR(10) NOT NULL,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### 6. `redis`

* Yorum metnini anahtar, analiz sonucunu değer olarak cache eder.

### 7. `kafka` ve `zookeeper`

* Topic'ler arında mesaj akışı sağlar:

  * `raw-comments`
  * `processed-comments`

---

## 🚀 Kurulum

### ✅ Gereklilikler

* Docker & Docker Compose

### 🔧 Kurulum Adımları

1. `.env` dosyasını oluşturun:

```env
KAFKA_BROKER=kafka:9092
RAW_TOPIC=raw-comments
PROCESSED_TOPIC=processed-comments

REDIS_HOST=redis
REDIS_PORT=6379

POSTGRES_DB=sentiment
POSTGRES_USER=admin
POSTGRES_PASSWORD=admin
POSTGRES_HOST=postgres
POSTGRES_PORT=5432

GRPC_HOST=grpc_service
GRPC_PORT=50051
```

2. Docker Compose ile tüm servisleri başlatın:

```bash
docker-compose up -d --build
```

> ⚠️ Servisler başlarken `healthcheck` ve `depends_on.condition: service_healthy` kullanılır.

3. Producer'la test edin:

```bash
docker exec -it sentiment-producer python producer.py
```

---

## 📂 Proje Yapısı

```
task_2/
├── config.py
├── .env
├── docker-compose.yml
├── producer/
│   ├── producer.py
│   └── Dockerfile
├── consumer/
│   ├── consumer.py
│   └── Dockerfile
├── grpc_service/
│   ├── sentiment.proto
│   ├── sentiment_service.py
│   ├── sentiment_pb2.py
│   ├── sentiment_pb2_grpc.py
│   └── Dockerfile
├── rest_api/
│   ├── main.py
│   ├── models/
│   │   ├── comment_model.py
│   │   └── comment_schema.py
│   ├── db/
│   │   └── database.py
│   └── Dockerfile
```

---

## 🔗 Bağlantılar

| Servis       | Adres                                                            |
| ------------ | ---------------------------------------------------------------- |
| REST API     | [http://localhost:8000/comments](http://localhost:8000/comments) |
| PostgreSQL   | localhost:5432 (admin/admin)                                     |
| Redis        | redis:6379                                                       |
| gRPC Service | grpc\_service:50051                                              |
| Kafka UI     | (Opsiyonel eklerseniz)                                           |

---

## 💡 Notlar ve Geliştirme Önerileri

* Kafka'ya GUI eklenebilir (Conduktor, Redpanda, Kowl)
* Sentiment gRPC servisi ML modeli ile geliştirilebilir
* Redis kullanımı ölçülebilir hale getirilebilir (TTL analiz)
* Otomatik testler, log takibi ve metrics (Prometheus + Grafana) eklenebilir

