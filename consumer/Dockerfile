FROM python:3.10-slim

WORKDIR /app

COPY consumer/consumer.py .
COPY grpc_service/sentiment_pb2.py grpc_service/sentiment_pb2_grpc.py .
COPY config.py . 
COPY .env .

RUN pip install kafka-python grpcio protobuf redis psycopg2-binary python-dotenv

CMD ["python", "consumer.py"]