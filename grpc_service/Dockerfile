FROM python:3.10-slim

WORKDIR /app

COPY grpc_service/sentiment_service.py .
COPY grpc_service/sentiment_pb2.py .
COPY grpc_service/sentiment_pb2_grpc.py .

RUN pip install grpcio grpcio-tools protobuf

CMD ["python", "sentiment_service.py"]