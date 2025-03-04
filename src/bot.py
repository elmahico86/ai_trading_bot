# bot.py

from src.trading_api import KucoinAPI
from src.data_manager import DataManager
from src.indicators import calculate_sma, calculate_ema, calculate_rsi
from src.model import TradingModel
import pandas as pd

class TradingBot:
    def __init__(self):
        self.api = KucoinAPI()
        self.data_manager = DataManager()
        self.model = TradingModel()

    def run(self, symbol, trade_amount):
        # Recupera i dati di mercato
        market_data = self.api.get_market_data(symbol)
        data_frame = pd.DataFrame([market_data])

        # Calcola gli indicatori tecnici
        data_frame['sma'] = calculate_sma(data_frame, window=14)
        data_frame['ema'] = calculate_ema(data_frame, window=14)
        data_frame['rsi'] = calculate_rsi(data_frame)

        # Prepara i dati per il modello
        # data = preprocess(data_frame)

        # Effettua la previsione
        # prediction = self.model.predict(data)

        # Strategia di trading basata sulla previsione
        # if prediction > soglia:
        #     self.execute_trade(symbol, 'buy', trade_amount)
        # elif prediction < soglia:
        #     self.execute_trade(symbol, 'sell', trade_amount)

    def execute_trade(self, symbol, side, amount):
        order = self.api.place_order(symbol, side, amount)
        price = order['dealFunds'] / order['dealSize']
        self.data_manager.store_trade(symbol, side, amount, price)
        print(f"Eseguito ordine {side} per {amount} {symbol} a {price}")

