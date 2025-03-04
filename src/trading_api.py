# trading_api.py

class KucoinAPI:
    # ...
    def get_historical_data(self, symbol, timeframe):
        try:
            # Mappa dei timeframe per KuCoin
            timeframe_mapping = {
                '1min': '1min',
                '5min': '5min',
                '15min': '15min',
                '30min': '30min',
                '1hour': '1hour',
                '4hour': '4hour',
                '1day': '1day'
            }
            kline = self.client.get_kline_data(
                symbol=symbol,
                kline_type=timeframe_mapping[timeframe]
            )
            return kline
        except Exception as e:
            raise Exception(f"Errore nel recupero dei dati storici: {e}")
