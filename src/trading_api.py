# trading_api.py

from kucoin.client import Client
from src.config import API_KEY, API_SECRET, API_PASSPHRASE, PAPER_TRADING

class KucoinAPI:
    def __init__(self):
        # Configura l'endpoint in base alla modalità di trading
        if PAPER_TRADING:
            self.client = Client(
                API_KEY, API_SECRET, API_PASSPHRASE,
                url='https://openapi-sandbox.kucoin.com'
            )
        else:
            self.client = Client(
                API_KEY, API_SECRET, API_PASSPHRASE,
                url='https://api.kucoin.com'
            )

    def place_order(self, symbol, side, size):
        try:
            order = self.client.create_market_order(
                symbol=symbol,
                side=side,
                size=size
            )
            return order
        except Exception as e:
            raise Exception(f"Errore nell'esecuzione dell'ordine: {e}")

    def get_market_data(self, symbol):
        try:
            data = self.client.get_ticker(symbol)
            return data
        except Exception as e:
            raise Exception(f"Errore nel recupero dei dati di mercato: {e}")
