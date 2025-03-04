# trading_api.py

from kucoin.client import Client
from src.config import API_KEY, API_SECRET, API_PASSPHRASE, PAPER_TRADING
import time

class KucoinAPI:
    def __init__(self):
        # Configura il client con le credenziali API
        self.client = Client(API_KEY, API_SECRET, API_PASSPHRASE)

    def place_order(self, symbol, side, size):
        """
        Esegue un ordine di mercato sul mercato specificato.
        Se in modalità paper trading, utilizza l'endpoint di test.
        """
        endpoint = '/api/v1/orders'
        if PAPER_TRADING:
            endpoint = '/api/v1/orders/test'

        order_params = {
            'clientOid': str(int(time.time() * 1000)),
            'side': side,
            'symbol': symbol,
            'type': 'market',
            'size': size
        }

        try:
            response = self.client._request('POST', endpoint, order_params)
            return response
        except Exception as e:
            raise Exception(f"Errore nell'esecuzione dell'ordine: {e}")

    def get_market_data(self, symbol):
        """
        Recupera i dati di mercato attuali per il simbolo specificato.
        """
        try:
            data = self.client.get_ticker(symbol)
            return data
        except Exception as e:
            raise Exception(f"Errore nel recupero dei dati di mercato: {e}")

    def get_historical_data(self, symbol, timeframe, limit=200):
        """
        Recupera i dati storici (kline) per il simbolo e il timeframe specificati.
        """
        try:
            kline_data = self.client.get_kline_data(symbol, kline_type=timeframe, limit=limit)
            data = []
            for kline in kline_data:
                data.append({
                    'timestamp': int(kline[0]),
                    'open': float(kline[1]),
                    'close': float(kline[2]),
                    'high': float(kline[3]),
                    'low': float(kline[4]),
                    'volume': float(kline[5])
                })
            return data[::-1]  # Ordina i dati dal più vecchio al più recente
        except Exception as e:
            raise Exception(f"Errore nel recupero dei dati storici: {e}")

    def get_all_tickers(self):
        """
        Recupera tutte le coppie di trading disponibili.
        """
        try:
            tickers = self.client.get_all_tickers()
            return tickers
        except Exception as e:
            raise Exception(f"Errore nel recupero dei ticker: {e}")

    def get_usdt_pairs(self):
        """
        Recupera tutte le coppie di trading che terminano con '-USDT'.
        """
        try:
            tickers = self.get_all_tickers()
            usdt_pairs = [ticker for ticker in tickers['ticker'] if ticker['symbol'].endswith('-USDT')]
            return usdt_pairs
        except Exception as e:
            raise Exception(f"Errore nel recupero delle coppie USDT: {e}")

    def get_account_overview(self):
        """
        Recupera una panoramica dell'account, inclusi fondi disponibili.
        """
        try:
            account = self.client.get_account_overview('USDT')
            return account
        except Exception as e:
            raise Exception(f"Errore nel recupero delle informazioni sull'account: {e}")
