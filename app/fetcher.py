import os
import asyncio

from api.orderbook_api_client import OrderBookAPIClient, BinanceAPIClient
from kafka_pc.producer import Producer

SLEEP_INTERVAL = int(os.environ.get('SLEEP_INTERVAL'))
TOPIC = os.environ.get('TOPIC')
BOOTSTRAP_SERVERS = os.environ.get('KAFKA_BROKER_ADDRESSES')
SYMBOL = os.environ.get('SYMBOL')

class Fetcher:
    @staticmethod
    async def fetch_orderbook(api_client: OrderBookAPIClient, producer: Producer, symbols: list = []):
        while True:
            data = await api_client.fetch_data(symbols)
            if data:
                producer.produce_orderbook(TOPIC, data)

            await asyncio.sleep(SLEEP_INTERVAL)

if __name__ == "__main__":
    api_client = BinanceAPIClient()
    kafka_producer = Producer(bootstrap_servers=BOOTSTRAP_SERVERS)
    symbols = [SYMBOL]

    asyncio.run(Fetcher.fetch_orderbook(api_client, kafka_producer, symbols))