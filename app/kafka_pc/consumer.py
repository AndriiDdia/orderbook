import json

from kafka import KafkaConsumer

class Consumer:
    def __init__(self, topic: str, bootstrap_servers : list = ['localhost:9092'], offset:str = "latest"):
        self.consumer = KafkaConsumer(
            topic,
            bootstrap_servers=bootstrap_servers,
            auto_offset_reset=offset,
            enable_auto_commit=True,
            value_deserializer=lambda x: json.loads(x.decode('utf-8'))
        )

    def get_latest_message(self):
        for message in self.consumer:
            message_data = message.value
            data = message_data.get('data', {})
            return data