import json

from kafka import KafkaProducer

class Producer:
    def __init__(self, bootstrap_servers : list = ['localhost:9092']):
        self.producer = KafkaProducer(
            bootstrap_servers=bootstrap_servers,
            key_serializer=lambda x: json.dumps(x).encode('utf-8'),
            value_serializer=lambda x: json.dumps(x).encode('utf-8')
        )

    def produce_orderbook(self, topic: str, orderbook_data: list = []):
        for item in orderbook_data:
            key = item["data"]["lastUpdateId"]
            print("fetch new data for item:", key, item["symbol"])
            self.send_message(topic, key, item)

    def send_message(self, topic: str, key: str, value: any):
        self.producer.send(topic, key=key, value=value)