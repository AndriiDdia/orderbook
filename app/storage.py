import asyncio
import os

import pandas as pd
import asyncpg

from kafka_pc.consumer import Consumer


LEVELS_TO_SAVE = int(os.environ.get("LEVELS_TO_SAVE"))
TOPIC = os.environ.get("TOPIC")
BOOTSTRAP_SERVERS = os.environ.get("KAFKA_BROKER_ADDRESSES")
POSTGRES_HOST = os.environ.get("POSTGRES_HOST")
POSTGRES_USER = os.environ.get("POSTGRES_USER")
POSTGRES_PASSWORD = os.environ.get("POSTGRES_PASSWORD")
POSTGRES_DB = os.environ.get("POSTGRES_DB")
SYMBOL = os.environ.get("SYMBOL")

POSTGRES_DSN = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:5432/{POSTGRES_DB}"


async def store_dataframe(conn, df, table_name):
    data_tuples = df.to_records(index=False).tolist()
    columns = ', '.join(df.columns)
    query = f"INSERT INTO {table_name} ({columns}) VALUES ($1, $2, $3, $4)"
    
    async with conn.transaction():
        await conn.executemany(query, data_tuples)

async def consume_and_store():
    kafka_consumer = Consumer(TOPIC, bootstrap_servers=BOOTSTRAP_SERVERS)
    conn = await asyncpg.connect(dsn=POSTGRES_DSN)
    
    try:
        while True:
            for message in kafka_consumer.consumer:
                message_data = message.value.get('data', {})

                ask_df = pd.DataFrame(message_data["asks"], columns=["price", "amount"], dtype=float)
                bid_df = pd.DataFrame(message_data["bids"], columns=["price", "amount"], dtype=float)
                ask_df = ask_df.iloc[-LEVELS_TO_SAVE:]
                bid_df = bid_df.iloc[:LEVELS_TO_SAVE]
                ask_df["order_type"] = "sell"
                bid_df["order_type"] = "buy"
                result_df = pd.concat([ask_df, bid_df], ignore_index=True)
                result_df["symbol"] = SYMBOL

                await store_dataframe(conn, result_df, table_name="order_book")

    finally:
        kafka_consumer.consumer.close()
        await conn.close()


if __name__ == "__main__":
    asyncio.run(consume_and_store())
