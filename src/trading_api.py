# trading_api.py

import time
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
        """
        Esegue un ordine di mercato sul mercato specificato.

        :param symbol: La coppia di trading, ad esempio 'BTC-USDT'.
        :param side: 'buy' o 'sell'.
        :param size: Quantità della valuta da acquistare/vendere.
        :return: Dettagli dell'ordine eseguito.
        """
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
        """
        Recupera i dati di mercato attuali per il simbolo specificato.

        :param symbol: La coppia di trading, ad esempio 'BTC-USDT'.
        :return: Dati di mercato correnti.
        """
        try:
            data = self.client.get_ticker(symbol)
            return data
        except Exception as e:
            raise Exception(f"Errore nel recupero dei dati di mercato: {e}")

    def get_historical_data(self, symbol, timeframe, limit=200):
        """
        Recupera i dati storici (kline) per il simbolo e il timeframe specificati.

        :param symbol: La coppia di trading, ad esempio 'BTC-USDT'.
        :param timeframe: Intervallo di tempo, ad esempio '1min', '5min', '1hour'.
        :param limit: Numero di candele da recuperare (massimo 200 per richiesta).
        :return: Lista di dizionari con i dati storici.
        """
        try:
            # Mappa dei timeframe per KuCoin
            timeframe_mapping = {
                '1min': '1min',
                '3min': '3min',
                '5min': '5min',
                '15min': '15min',
                '30min': '30min',
                '1hour': '1hour',
                '2hour': '2hour',
                '4hour': '4hour',
                '6hour': '6hour',
                '8hour': '8hour',
                '12hour': '12hour',
                '1day': '1day',
                '1week': '1week'
            }
            if timeframe not in timeframe_mapping:
                raise ValueError("Timeframe non supportato.")

            # Ottiene il timestamp corrente
            end_at = int(time.time())
            # Calcola il timestamp di inizio in base al limite e al timeframe
            interval_seconds = self.timeframe_to_seconds(timeframe)
            start_at = end_at - (limit * interval_seconds)

            # Ottiene i dati storici (kline)
            klines = self.client.get_kline_data(
                symbol=symbol,
                kline_type=timeframe_mapping[timeframe],
                start=str(start_at),
                end=str(end_at)
            )

            # Converte i dati in un formato utilizzabile
            data = []
            for kline in klines:
                # kline contiene: [timestamp, open, close, high, low, volume, turnover]
                data.append({
                    'timestamp': int(kline[0]),
                    'open': float(kline[1]),
                    'close': float(kline[2]),
                    'high': float(kline[3]),
                    'low': float(kline[4]),
                    'volume': float(kline[5]),
                    'turnover': float(kline[6])
                })

            return data[::-1]  # Inverte la lista per avere i dati in ordine cronologico crescente

        except Exception as e:
            raise Exception(f"Errore nel recupero dei dati storici: {e}")

    def timeframe_to_seconds(self, timeframe):
        """
        Converte il timeframe in secondi.

        :param timeframe: Stringa del timeframe, ad esempio '1min', '1hour'.
        :return: Numero di secondi corrispondenti al timeframe.
        """
        unit = ''.join(filter(str.isalpha, timeframe))
        value = int(''.join(filter(str.isdigit, timeframe)))
        conversion = {
            'min': 60,
            'hour': 3600,
            'day': 86400,
            'week': 604800
        }
        if unit in conversion:
            return value * conversion[unit]
        else:
            raise ValueError("Unità di tempo non supportata.")

    def get_all_tickers(self):
        """
        Recupera tutte le coppie di trading disponibili.

        :return: Dati di tutti i ticker.
        """
        try:
            tickers = self.client.get_all_tickers()
            return tickers
        except Exception as e:
            raise Exception(f"Errore nel recupero dei ticker: {e}")

    def get_account_overview(self):
        """
        Recupera una panoramica dell'account, inclusi fondi disponibili.

        :return: Dati dell'account.
        """
        try:
            account = self.client.get_account_overview('BTC')
            return account
        except Exception as e:
            raise Exception(f"Errore nel recupero delle informazioni sull'account: {e}")

