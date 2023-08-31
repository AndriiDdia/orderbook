import asyncio
import aiohttp
from abc import ABC, abstractmethod


class OrderBookAPIClient(ABC):
    @abstractmethod
    def fetch_data(self, symbols: list = []):
        pass


class BinanceAPIClient(OrderBookAPIClient):
    # API_URL = "https://testnet.binancefuture.com/fapi/v1/depth"
    API_URL = "https://api.binance.com/api/v3/depth"

    async def _fetch_orderbook_data(self, session: aiohttp.ClientSession, url: str = API_URL, params: list = []):
        async with session.get(url, params=params) as response:
            data = await response.json()
            return data

    async def fetch_data(self, symbols: list = []):
        params_list = [
            {
                "symbol": symbol,
                "limit": 1000
            } for symbol in symbols
        ]

        async with aiohttp.ClientSession() as session:
            tasks = [self._fetch_orderbook_data(session, BinanceAPIClient.API_URL, param) for param in params_list]
            response = await asyncio.gather(*tasks)

            results = []
            for param, result in zip(params_list, response):
                results.append({
                    "symbol": param["symbol"],
                    "data": result
                })
            
            return results
