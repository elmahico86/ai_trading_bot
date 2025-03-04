# data_manager.py

import sqlite3
import os

class DataManager:
    def __init__(self, db_path='data/trading_data.db'):
        self.db_path = db_path
        self.connection = None
        self._initialize_database()

    def _initialize_database(self):
        if not os.path.exists('data'):
            os.makedirs('data')
        self.connection = sqlite3.connect(self.db_path)
        cursor = self.connection.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS trades (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                symbol TEXT,
                side TEXT,
                size REAL,
                price REAL,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        self.connection.commit()

    def store_trade(self, symbol, side, size, price):
        cursor = self.connection.cursor()
        cursor.execute('''
            INSERT INTO trades (symbol, side, size, price)
            VALUES (?, ?, ?, ?)
        ''', (symbol, side, size, price))
        self.connection.commit()

    def get_trade_history(self):
        cursor = self.connection.cursor()
        cursor.execute('SELECT * FROM trades ORDER BY timestamp DESC')
        return cursor.fetchall()
