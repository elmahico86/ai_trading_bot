# bot.py

import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.models import load_model
from src.trading_api import KucoinAPI
from src.data_manager import DataManager
from src.indicators import calculate_indicators
from src.model import TradingModel
from src.risk_manager import RiskManager
from src.config import TRADE_SYMBOLS, TRADE_TIMEFRAMES, PAPER_TRADING

class TradingBot:
    def __init__(self):
        self.api = KucoinAPI()
        self.data_manager = DataManager()
        self.model = TradingModel()
        self.risk_manager = RiskManager()
        self.scaler = MinMaxScaler()

    def run(self):
        for symbol in TRADE_SYMBOLS:
            for timeframe in TRADE_TIMEFRAMES:
                # Recupera i dati storici
                market_data = self.api.get_historical_data(symbol, timeframe)
                data_frame = pd.DataFrame(market_data)

                # Calcola gli indicatori tecnici
                data_frame = calculate_indicators(data_frame)

                # Prepara i dati per il modello
                data_frame.dropna(inplace=True)
                X, y = self.prepare_data(data_frame)

                # Addestra il modello
                X_train, X_val, y_train, y_val = self.train_test_split(X, y)
                self.model.train(X_train, y_train, X_val, y_val)

                # Effettua la previsione
                prediction = self.model.predict(X[-1:])
                prediction = prediction[0][0]

                # Gestione del rischio
                account_balance = self.api.get_account_overview()['availableBalance']
                stop_loss_pips = self.calculate_stop_loss_pips(data_frame)
                position_size = self.risk_manager.calculate_position_size(float(account_balance), stop_loss_pips)

                # Decisione di trading
                if self.risk_manager.check_daily_drawdown(float(account_balance)):
                    self.make_decision(symbol, prediction, position_size)

    def prepare_data(self, data_frame):
        features = data_frame.drop(['close', 'timestamp'], axis=1)
        target = data_frame['close']
        features_scaled = self.scaler.fit_transform(features)
        target_scaled = self.scaler.fit_transform(target.values.reshape(-1, 1))
        return features_scaled, target_scaled

    def train_test_split(self, X, y, test_size=0.2):
        split_index = int(len(X) * (1 - test_size))
        X_train, X_val = X[:split_index], X[split_index:]
        y_train, y_val = y[:split_index], y[split_index:]
        return X_train, X_val, y_train, y_val

    def calculate_stop_loss_pips(self, data_frame):
        # Calcola l'ATR per determinare lo stop loss
        atr = data_frame['atr'].iloc[-1]
        return atr

    def make_decision(self, symbol, prediction, position_size):
        # Strategia di trading basata sulla previsione
        if prediction > 0.5:
            side = 'buy'
        elif prediction < -0.5:
            side = 'sell'
        else:
            print(f"Nessuna opportunità di trading per {symbol}")
            return

        # Esegue il trade
        self.execute_trade(symbol, side, position_size)

    def execute_trade(self, symbol, side, amount):
        response = self.api.place_order(symbol, side, amount)
        if not PAPER_TRADING:
            executed_price = float(response['dealFunds']) / float(response['dealSize'])
            self.data_manager.store_trade(symbol, side, amount, executed_price)
            print(f"Eseguito ordine {side} per {amount} {symbol} a {executed_price}")
        else:
            print(f"Ordine di test {side} per {amount} {symbol}")
