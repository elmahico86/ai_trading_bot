# bot.py

from src.trading_api import KucoinAPI
from src.data_manager import DataManager
from src.indicators import calculate_indicators  # Assumendo che sia stato aggiornato
from src.model import TradingModel
from src.config import SYMBOL, TRADE_AMOUNT
import pandas as pd

class TradingBot:
    def __init__(self):
        self.api = KucoinAPI()
        self.data_manager = DataManager()
        self.model = TradingModel()

    def run(self):
        # Recupera i dati di mercato
        market_data = self.api.get_historical_data(SYMBOL, '1min', limit=100)
        data_frame = pd.DataFrame(market_data)

        # Calcola gli indicatori tecnici
        data_frame = calculate_indicators(data_frame)

        # Prepara i dati per il modello
        X, y = self.prepare_data(data_frame)

        # Effettua la previsione
        prediction = self.model.predict(X[-1:])

        # Prende decisioni di trading basate sulla previsione
        self.make_decision(SYMBOL, prediction)

    def prepare_data(self, data_frame):
        # Preprocessing dei dati
        features = data_frame.drop(['close', 'timestamp'], axis=1).values
        target = data_frame['close'].values
        return features, target

    def make_decision(self, symbol, prediction):
        # Strategia di trading basata sulla previsione
        # Implementa la logica per decidere se comprare o vendere
        if prediction > some_threshold:
            self.execute_trade(symbol, 'buy', TRADE_AMOUNT)
        elif prediction < some_other_threshold:
            self.execute_trade(symbol, 'sell', TRADE_AMOUNT)

    def execute_trade(self, symbol, side, amount):
        response = self.api.place_order(symbol, side, amount)
        if not PAPER_TRADING:
            price = float(response['dealFunds']) / float(response['dealSize'])
            self.data_manager.store_trade(symbol, side, amount, price)
        print(f"Ordine {'di test' if PAPER_TRADING else ''} {side} per {amount} {symbol}")

