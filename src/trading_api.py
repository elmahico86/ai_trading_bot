# src/trading_api.py

import aiohttp
import asyncio
import logging
from config import API_KEY, API_SECRET, ENVIRONMENT

class TradingAPI:
    def __init__(self):
        self.api_key = API_KEY
        self.api_secret = API_SECRET
        self.base_url = 'https://paper-api.alpaca.markets' if ENVIRONMENT == 'paper' else 'https://api.alpaca.markets'
        self.headers = {
            'APCA-API-KEY-ID': self.api_key,
            'APCA-API-SECRET-KEY': self.api_secret
        }
        self.session = aiohttp.ClientSession(headers=self.headers)
        self.logger = logging.getLogger('TradingAPI')

    async def place_order(self, symbol, qty, side, type='market', time_in_force='gtc'):
        url = f'{self.base_url}/v2/orders'
        order = {
            'symbol': symbol,
            'qty': qty,
            'side': side,
            'type': type,
            'time_in_force': time_in_force
        }
        for attempt in range(5):
            try:
                async with self.session.post(url, json=order) as resp:
                    if resp.status == 200:
                        response = await resp.json()
                        self.logger.info(f"Ordine piazzato: {response}")
                        return response
                    else:
                        error = await resp.text()
                        self.logger.error(f"Errore API ({resp.status}): {error}")
                        if resp.status in [500, 502, 503, 504]:
                            await asyncio.sleep(2 ** attempt)
                            continue
                        else:
                            break
            except aiohttp.ClientError as e:
                self.logger.error(f"Errore di connessione: {e}")
                await asyncio.sleep(2 ** attempt)
        return None

    async def get_position(self, symbol):
        url = f'{self.base_url}/v2/positions/{symbol}'
        async with self.session.get(url) as resp:
            if resp.status == 200:
                position = await resp.json()
                return position
            else:
                return None

    async def close(self):
        await self.session.close()
