import threading
from lru_cache import LRUCache
from connectors import KafkaConnector


def create_cache(max_size=5, exp_time_in_min=5, broker=""):
    cache = LRUCache(max_size=max_size, exp_time_in_min=exp_time_in_min)
    connector = KafkaConnector(broker, cache)
    expiration_timer_thread = threading.Thread(target=cache.start_expiration_timer, daemon=True)
    producer_thread = threading.Thread(target=connector.publish, daemon=True)
    consumer_thread = threading.Thread(target=connector.fetch, daemon=True)
    expiration_timer_thread.start()
    producer_thread.start()
    consumer_thread.start()
    return cache
