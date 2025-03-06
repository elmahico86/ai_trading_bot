import time
import requests
from kucoin.client import Client
from src.config import API_KEY, API_SECRET, API_PASSPHRASE, PAPER_TRADING

class KucoinAPI:
    def __init__(self):
        # Configura il client con le credenziali API
        self.client = Client(API_KEY, API_SECRET, API_PASSPHRASE)

    def place_order(self, symbol, side, size):
        """
        Esegue un ordine di mercato sul simbolo specificato.
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

    def get_historical_data(self, symbol, timeframe, limit=100):
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

    def get_large_history(self, symbol, timeframe, total_limit=1000):
        """
        Recupera un dataset ampio di candele storiche accumulando richieste multiple.
        Assicura che il dataset finale sia ordinato cronologicamente.

        Args:
            symbol (str): Il simbolo (es. 'BTC-USDT').
            timeframe (str): Il timeframe (es. '1min', '5min', '15min').
            total_limit (int): Il numero totale di candele desiderate (default: 1000).

        Returns:
            list: Lista di candele accumulate (ogni candela è un dizionario con valori OHLCV).
        """
        candles = []
        limit_per_request = 100  # Limite massimo per richiesta
        end_time = None  # Impostato a None per la prima richiesta

        while len(candles) < total_limit:
            try:
                # Esegui la richiesta
                if end_time is not None:
                    data = self.client.get_kline_data(symbol, kline_type=timeframe, limit=limit_per_request, endTime=end_time)
                else:
                    data = self.client.get_kline_data(symbol, kline_type=timeframe, limit=limit_per_request)

                print(f"Richiesta effettuata: ottenute {len(data)} candele per {symbol} ({timeframe})")

                if not data:
                    break  # Esce se non ci sono più dati disponibili

                # Aggiungi i dati in ordine cronologico crescente
                candles.extend(data[::-1])

                # Aggiorna end_time al timestamp della candela più antica ottenuta
                end_time = data[0][0]

                # Interrompi il ciclo se la richiesta restituisce meno di limit_per_request (dati esauriti)
                if len(data) < limit_per_request:
                    break

            except Exception as e:
                print(f"Errore durante il recupero dei dati: {e}")
                break

        # Assicuriamoci che le candele siano ordinate cronologicamente
        candles.sort(key=lambda x: x[0])  # Ordina per timestamp
        print(f"Totale candele accumulate per {symbol} ({timeframe}): {len(candles)}")
        return candles[:total_limit]

    def get_all_tickers(self):
        """
        Recupera tutti i ticker disponibili utilizzando l'endpoint REST di KuCoin.
        """
        try:
            url = "https://api.kucoin.com/api/v1/market/allTickers"
            response = requests.get(url)
            if response.status_code == 200:
                data = response.json()
                if isinstance(data, dict) and "data" in data and "ticker" in data["data"]:
                    return data["data"]["ticker"]
                else:
                    return data
            else:
                raise Exception(f"Errore nel recupero dei ticker: {response.text}")
        except Exception as e:
            raise Exception(f"Errore nel recupero dei ticker: {e}")

    def get_usdt_pairs(self):
        """
        Recupera tutte le coppie di trading che terminano con '-USDT'.
        """
        try:
            tickers = self.get_all_tickers()
            if isinstance(tickers, list):
                usdt_pairs = [ticker for ticker in tickers if ticker.get('symbol', '').endswith('-USDT')]
            else:
                usdt_pairs = []
            return usdt_pairs
        except Exception as e:
            raise Exception(f"Errore nel recupero delle coppie USDT: {e}")

    def get_account_overview(self):
        """
        Recupera il saldo disponibile per USDT utilizzando il metodo get_accounts.
        Filtra per l'account di tipo 'trade' se disponibile.
        """
        try:
            accounts = self.client.get_accounts(currency="USDT")
            if isinstance(accounts, list) and accounts:
                for acc in accounts:
                    if acc.get('type') == 'trade':
                        return acc
                return accounts[0]
            else:
                raise Exception("Nessun account trovato per USDT")
        except Exception as e:
            raise Exception(f"Errore nel recupero delle informazioni sull'account: {e}")
