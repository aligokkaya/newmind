import grpc
from concurrent import futures
import time
import random
import threading

import sentiment_pb2
import sentiment_pb2_grpc



class RateLimiter:
    def __init__(self, max_requests_per_sec):
        self.capacity = max_requests_per_sec
        self.tokens = max_requests_per_sec
        self.lock = threading.Lock()
        self.last_refill = time.time()

    def allow_request(self):
        with self.lock:
            now = time.time()
            elapsed = now - self.last_refill
            refill = int(elapsed * self.capacity)
            if refill > 0:
                self.tokens = min(self.capacity, self.tokens + refill)
                self.last_refill = now
            if self.tokens > 0:
                self.tokens -= 1
                return True
            return False


class SentimentAnalyzer(sentiment_pb2_grpc.SentimentAnalyzerServicer):
    def __init__(self):
        self.cache = {}
        self.ratelimiter = RateLimiter(100)

    def Analyze(self, request, context):
        text = request.text.strip()

        # Rate limit kontrolü
        if not self.ratelimiter.allow_request():
            context.set_code(grpc.StatusCode.RESOURCE_EXHAUSTED)
            context.set_details('Rate limit exceeded')
            return sentiment_pb2.SentimentResponse()

        # Rastgele drop (örn. %5 olasılıkla)
        if random.random() < 0.05:
            context.set_code(grpc.StatusCode.UNAVAILABLE)
            context.set_details('Random drop simulated')
            return sentiment_pb2.SentimentResponse()

        # Daha önce varsa cache'ten al
        if text in self.cache:
            result = self.cache[text]
        else:
            result = random.choice(['positive', 'negative', 'neutral'])
            self.cache[text] = result

        time.sleep(len(text) * 0.01)

        return sentiment_pb2.SentimentResponse(sentiment=result)


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    sentiment_pb2_grpc.add_SentimentAnalyzerServicer_to_server(SentimentAnalyzer(), server)
    server.add_insecure_port('0.0.0.0:50051')
    print("SentimentService gRPC sunucusu 50051 portunda çalışıyor...")
    server.start()
    server.wait_for_termination()

serve()