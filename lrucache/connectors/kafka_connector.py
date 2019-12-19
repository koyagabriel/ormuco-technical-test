import uuid
import json
from confluent_kafka import Producer, Consumer
from confluent_kafka.admin import AdminClient, NewTopic


class KafkaConnector:

    DEFAULT_TOPIC = 'cache_topic'

    def __init__(self, broker, cache):
        if not isinstance(broker, str):
            raise TypeError("broker should be of type string")

        self._create_topic(broker)
        self._producer = Producer({'bootstrap.servers': broker})
        self._group_id = str(uuid.uuid4())
        self._consumer = Consumer({
            'bootstrap.servers': broker,
            'group.id': self._group_id,
            'auto.offset.reset': 'latest'
        })
        self._consumer.subscribe([self.DEFAULT_TOPIC])
        self._cache = cache

    def _create_topic(self, broker):
        admin_client = AdminClient({'bootstrap.servers': broker})

        if not self.DEFAULT_TOPIC in admin_client.list_topics().topics:
            new_topic = NewTopic(self.DEFAULT_TOPIC,
                                 num_partitions=3, replication_factor=1)
            fs = admin_client.create_topics([new_topic])

            for topic, value in fs.items():
                try:
                    value.result()
                except Exception as e:
                    raise Exception('Unable to create topic for cache')

    def _delivery_report(self, error, message):
        if error is not None:
            print(f'Message delivery failed {error}')
        else:
            print(
                f'Message delivered to {message.topic()} [{message.partition()}]')

    def publish(self):
        while True:
            data = self._cache.get_next_event_data()
            if data:
                data.update(group_id=self._group_id)
                self._producer.poll(0)
                self._producer.produce(self.DEFAULT_TOPIC, json.dumps(
                    data).encode('utf-8'), callback=self._delivery_report)
        self._producer.flush()

    def fetch(self):
        while True:
            msg = self._consumer.poll(0)

            if msg and msg.error():
                print(f"Consumer error: {msg.error}")
                return

            if msg:
                data = json.loads(msg.value().decode('utf-8'))
                group_id = data.pop('group_id')
                if group_id != self._group_id:
                    self._cache.process_event_data(data)
                    print(f"Received message: {data}")

        self._consumer.close()
