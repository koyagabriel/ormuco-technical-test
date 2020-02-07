## Geo Distributed LRU Cache
The Cache library is a cache designed to be used in a distributed environment, that is , an environment setup with multiple machines separated by geographical locations. It replicates data across geolocation, maintains data consistency across regions and writes these data in real time by leveraging on kafka's messaging, storage and real time replication functionalities.

## Design

An overview of the design will be broken down based on the design requirements which are:
- Simplicity. Integration must be simple.
- Resilient to network failures or crashes.
- Near real time replication of data across geolocation.
- Data consistency across regions
- Locality of reference
- Flexible Schema

### Simplicity:
The library is easy to integrate. You only need to call an helper function that returns an instance of the cache.  The function take two arguments, which are `maximum size of the cache` and the `kafka broker url`
```
  from lrucache import create_cache

  cache_instance = create_cache(max_size, broker)
```

### Resilient to network failures or crashes
The cache leverages on kafka for data storage in order to achieve resilence to network failures as data written to kafka is written to disk and replicated for fault tolerance.

### Near real time replication of data across gelocation
The library makes use of kafka messaging/streaming system to replicate data in real time across mutiple cache instances seprated by geolocation.

### Data Consistency across regions
The library leverages on kafka messaging system to constantly communicate updates to remote caches when a cache makes changes locally. This ensure synchronization between caches.

### Locality of reference
Data is extracted from caches local to the system, while updates from remotes caches are gotten from kafka messaging system.

### Flexible Schema
Any data type can be stored in the cache.

### Operation Supported
The cache supports the following operations:
- `get(key):` gets the value of the key if the key exists in the cache, otherwise it returns None.
  ```
  from lrucache import create_cache
  cache_instance = create_cache(max_size=5, broker="localhost:9092")
  cache_instance.get(key)
  ```
- `add(key, value):` inserts the value if the key is not present. When the cache reaches its capacity, it invalidates the least recently used item before inserting a new item.
  ```
  from lrucache import create_cache
  cache_instance = create_cache(max_size=5, broker="localhost:9092")
  cache_instance.add(key, value)
  ```
- `update(key, value):` sets the value of a key to a new value if the key exits in the cache.
  ```
  from lrucache import create_cache
  cache_instance = create_cache(max_size=5, broker="localhost:9092")
  cache_instance.update(key, value)
  ```

### Data Structures used
- Dict: This data structure was used in order to achieve a O(1) lookup when performing the get and update operations.
- Doubly Linked List: This data structure was used in other to achieve an  0(1) complexity while deleting or inserting a node.


### Task yet to be completed
- writing test although it has been tested manually.
