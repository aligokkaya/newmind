# 🧠 Real-Time Sentiment Analysis Pipeline

Bu proje, gerçek zamanlı kullanıcı yorumlarını analiz eden mikroservis tabanlı bir veri işleme sistemidir. Kafka aracılığıyla toplanan yorumlar, gRPC üzerinden çalışan bir AI servisi ile analiz edilir, Redis ile önbelleğe alınır ve PostgreSQL'e kalıcı olarak kaydedilir. Kullanıcılar bu sonuçlara REST API üzerinden erişebilir.

---

## 📀 Mimarinin Genel Yapısı

```
Kullanıcı → Producer → Kafka (raw-comments)
                               ↓
                       Consumer → gRPC (Sentiment Service)
                               ↓
                    ↧ Redis       ↩ PostgreSQL
                                 ↓
                           FastAPI (REST API)
```

---

## 🧱 Kullanılan Teknolojiler

| Bileşen        | Açıklama                                               |
| -------------- | ------------------------------------------------------ |
| **Kafka**      | Yorumları publish-subscribe modeliyle taşır            |
| **gRPC**       | Yorumların duygu analizini yapan servis                |
| **Redis**      | Yorum metni bazlı sonuçları cache’ler                  |
| **PostgreSQL** | İşlenmiş yorumları kalıcı olarak saklar                |
| **FastAPI**    | İşlenmiş verileri dışa sunan RESTful API sağlar        |
| **Docker**     | Tüm bileşenleri kapsülleyip yönetir (`docker-compose`) |

---

## 🚀 Hızlı Başlangıç

### 1. Projeyi klonlayın

```bash
git clone https://github.com/kullanici/sentiment-pipeline.git
cd sentiment-pipeline
```

### 2. Docker imajlarını oluşturun

```bash
docker-compose build
```

### 3. Servisleri başlatın

```bash
docker-compose up
```

> Tüm servisler `docker-compose` kullanılarak ayağa kaldırılır: Kafka, Zookeeper, Redis, PostgreSQL, gRPC, Producer, Consumer ve REST API.

---

## 📊 Servisler

| Servis       | Port  | Açıklama                         |
| ------------ | ----- | -------------------------------- |
| Kafka        | 9092  | Mesajlaşma altyapısı             |
| Zookeeper    | 2181  | Kafka yönetimi için              |
| PostgreSQL   | 5432  | Veritabanı                       |
| Redis        | 6379  | Cache servisi                    |
| gRPC Service | 50051 | Duygu analizi için               |
| REST API     | 8000  | İşlenmiş verileri dışa sunan API |

---

## 📬 REST API Örnekleri

### Tüm yorumları listeleme

```http
GET http://localhost:8000/comments
```

### Belirli bir yorum sorgulama

```http
GET http://localhost:8000/comments/{comment_id}
```

---

## 🧠 Duygu Analizi (gRPC Servisi)

* gRPC servisi, `sentiment_pb2` ve `sentiment_pb2_grpc` üzerinden çağrılır.
* Örnek çağrı:

```python
request = SentimentRequest(text="Servis çok kötüydü.")
response = grpc_client.Analyze(request)
print(response.sentiment)  # "NEGATIVE"
```

---

## 💪 Docker Compose Yapısı

`docker-compose.yml` içerisinde aşağıdaki servisler tanımlıdır:

* `kafka`
* `zookeeper`
* `postgres`
* `redis`
* `grpc_service`
* `producer`
* `consumer`
* `rest_api`

Her bir servis için gerekli `Dockerfile` dosyaları `./producer`, `./consumer`, `./grpc_service`, `./rest_api` klasörlerinde yer alır.

---

## 🚲 Geliştirici Notları

* Tüm servisler kendi bağımsız container'ında çalışır.
* Kafka içinde `raw-comments` ve `processed-comments` olmak üzere iki topic kullanılır.
* Redis üzerinden sorgu performansı artırılır.
* `psycopg2`, `kafka-python`, `grpcio` gibi kütüphaneler kullanılır.
