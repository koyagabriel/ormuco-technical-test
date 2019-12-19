import json
from threading import RLock
from collections import deque


class LRUCache:
    PREVIOUS, NEXT, KEY, VALUE = 0, 1, 2, 3
    ADD = 'ADD'
    UPDATE = 'UPDATE'
    GET = 'GET'

    def __init__(self, max_size=5):

        if isinstance(max_size, int):
            if max_size < 0:
                raise TypeError('max_size should not be a negative value')
        else:
            raise TypeError('max_size should be an integer')

        self._cache = {}
        self._max_size = max_size
        self._full = False
        self._root = []
        self._root[:] = [self._root, self._root, None, None]
        self._event_queue = deque()
        self._lock = RLock()

    @property
    def cache(self):
        return self._cache

    @property
    def full(self):
        return self._full

    @property
    def max_size(self):
        return self._max_size

    @property
    def root(self):
        raise NotImplementedError("Property not implemented")

    def get(self, key, push_to_queue=True):
        with self._lock:
            result = self._cache.get(key)

            if not result:
                return result

            prev_link, next_link, _key, value = result
            prev_link[self.NEXT] = next_link
            next_link[self.PREVIOUS] = prev_link
            last = self._root[self.PREVIOUS]
            last[self.NEXT] = self._root[self.PREVIOUS] = result
            result[self.NEXT] = self._root
            result[self.PREVIOUS] = last

            if push_to_queue:
                self._queue_event_data(key, value, self.GET)

            return value

    def add(self, key, value, push_to_queue=True):
        with self._lock:
            error_msg = "Key already exist in the cache"
            if key in self._cache:
                raise ValueError(error_msg)

            if self._full:
                old_root = self._root
                old_root[self.KEY] = key
                old_root[self.VALUE] = value

                self._root = old_root[self.NEXT]
                old_key = self._root[self.KEY]
                old_value = self._root[self.VALUE]
                self._root[self.KEY] = self._root[self.VALUE] = None

                del self._cache[old_key]
                self._cache[key] = old_root
            else:
                last = self._root[self.PREVIOUS]
                result = [last, self._root, key, value]
                last[self.NEXT] = self._root[self.PREVIOUS] = self._cache[key] = result
                full = (len(self._cache) >= self._max_size)

            if push_to_queue:
                self._queue_event_data(key, value, self.ADD)

    def update(self, key, value, push_to_queue=True):
        with self._lock:
            if not key in self._cache:
                raise ValueError("Cache does not contain key")

            result = self._cache.get(key)
            result[self.VALUE] = value
            prev_link, next_link, _key, _value = result
            prev_link[self.NEXT] = next_link
            next_link[self.PREVIOUS] = prev_link
            last = self._root[self.PREVIOUS]
            result[self.NEXT] = self._root
            result[self.PREVIOUS] = last
            last[self.NEXT] = self._root[self.PREVIOUS] = self._cache[key] = result

            if push_to_queue:
                self._queue_event_data(key, value, self.UPDATE)

    def get_next_event_data(self):
        with self._lock:
            if len(self._event_queue):
                return self._event_queue.popleft()

    def _queue_event_data(self, key, value, event_type):
        self._event_queue.append({
            'key': key,
            'value': value,
            'type': event_type
        })

    def process_event_data(self, event_data):
        with self._lock:
            event_type = event_data['type']
            _key = event_data['key']
            value = event_data['value']
            if event_type == self.ADD:
                self.add(_key, value, push_to_queue=False)
            elif event_type == self.GET:
                self.get(_key, push_to_queue=False)
            elif event_type == self.UPDATE:
                self.update(_key, value, push_to_queue=False)

    def _cache_clear(self):
        with self._lock:
            self._cache.clear()
            self._root[:] = [self._root, self._root, None, None]
            self._full = False
