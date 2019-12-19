import threading
from lru_cache import LRUCache
from connectors import KafkaConnector

def create_cache(max_size=5, broker=""):
	cache = LRUCache(max_size=max_size)
	connector = KafkaConnector(broker, cache)
	producer_thread = threading.Thread(target=connector.publish, daemon=True)
	consumer_thread = threading.Thread(target=connector.fetch, daemon=True)
	producer_thread.start()
	consumer_thread.start()
	return cache
