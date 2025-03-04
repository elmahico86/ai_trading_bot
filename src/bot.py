# bot.py

from src.trading_api import KucoinAPI
from src.data_manager import DataManager
from src.indicators import calculate_indicators  # Funzione aggiornata
from src.model import TradingModel
import pandas as pd
import numpy as np

class TradingBot:
    def __init__(self):
        self.api = KucoinAPI()
        self.data_manager = DataManager()
        self.model = TradingModel()
        self.symbols = self.get_top_symbols()
        self.timeframes = ['1min', '5min', '15min']
        self.risk_manager = RiskManager()

    def get_top_symbols(self):
        # Ottiene le coppie con maggior volume e volatilità
        tickers = self.api.client.get_all_tickers()
        tickers_df = pd.DataFrame(tickers['ticker'])
        tickers_df['volatility'] = tickers_df['changeRate'].astype(float).abs()
        top_symbols = tickers_df.sort_values(['vol', 'volatility'], ascending=False)['symbol'].head(10).tolist()
        return top_symbols

    def run(self):
        for symbol in self.symbols:
            for timeframe in self.timeframes:
                # Recupera i dati storici per il simbolo e il timeframe
                market_data = self.api.get_historical_data(symbol, timeframe)
                data_frame = pd.DataFrame(market_data)
                data_frame = calculate_indicators(data_frame)

                # Prepara i dati per il modello
                X, y = self.prepare_data(data_frame)
                # Dividi in training e validation set
                X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=0.2)

                # Addestramento del modello
                self.model.train(X_train, y_train, X_val, y_val)

                # Previsione e decisione di trading
                prediction = self.model.predict(X[-1:])
                self.make_decision(symbol, prediction)

    def prepare_data(self, data_frame):
        # Preprocessing dei dati
        features = data_frame.drop(['close', 'time'], axis=1).values
        target = data_frame['close'].values
        return features, target

    def make_decision(self, symbol, prediction):
        # Strategia di trading basata sulla previsione e sul risk management
        position_size = self.risk_manager.calculate_position_size(prediction)
        if prediction > some_threshold:
            self.execute_trade(symbol, 'buy', position_size)
        elif prediction < some_threshold:
            self.execute_trade(symbol, 'sell', position_size)

    def execute_trade(self, symbol, side, amount):
        order = self.api.place_order(symbol, side, amount)
        price = float(order['dealFunds']) / float(order['dealSize'])
        self.data_manager.store_trade(symbol, side, amount, price)
        print(f"Eseguito ordine {side} per {amount} {symbol} a {price}")
