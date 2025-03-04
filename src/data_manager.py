# src/data_manager.py

import sqlite3
import pandas as pd
import numpy as np
from config import DATABASE_PATH
from indicators import compute_indicators
import asyncio
import aiohttp
import datetime
import os

class DataManager:
    def __init__(self):
        self.conn = sqlite3.connect(DATABASE_PATH, check_same_thread=False)
        self.cursor = self.conn.cursor()
        self.create_table()
        self.session = aiohttp.ClientSession()
        self.api_url = "https://api.marketdata.com/v1"
        self.api_key = os.getenv('MARKET_DATA_API_KEY')

    def create_table(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS market_data (
                timestamp DATETIME,
                symbol TEXT,
                open REAL,
                high REAL,
                low REAL,
                close REAL,
                volume REAL,
                PRIMARY KEY (timestamp, symbol)
            )
        ''')
        self.conn.commit()

    async def fetch_market_data(self, symbol, start_date, end_date):
        params = {
            'symbol': symbol,
            'start': start_date,
            'end': end_date,
            'api_key': self.api_key
        }
        url = f"{self.api_url}/historical"
        async with self.session.get(url, params=params) as response:
            data = await response.json()
            df = pd.DataFrame(data['prices'])
            df['symbol'] = symbol
            df.to_sql('market_data', self.conn, if_exists='append', index=False)
            return df

    def get_latest_data(self, symbol, lookback=TIME_STEPS):
        query = f'''
            SELECT * FROM market_data
            WHERE symbol = '{symbol}'
            ORDER BY timestamp DESC
            LIMIT {lookback}
        '''
        df = pd.read_sql_query(query, self.conn)
        df.sort_values('timestamp', inplace=True)
        return df

    def preprocess_data(self, df):
        df = compute_indicators(df)
        df.dropna(inplace=True)
        return df

    async def close(self):
        await self.session.close()
        self.conn.close()
