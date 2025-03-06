import pandas as pd
import numpy as np
import schedule
import time
import os
from sklearn.preprocessing import MinMaxScaler
from sklearn.ensemble import RandomForestRegressor
from src.trading_api import KucoinAPI
from src.data_manager import DataManager
from src.indicators import calculate_indicators
from src.model import TradingModel
from src.risk_manager import RiskManager
from src.config import NUM_TOP_PAIRS, TRADE_TIMEFRAMES, PAPER_TRADING, MIN_VOLUME, MAX_SPREAD_PERCENTAGE, CANDLE_LIMIT

class TradingBot:
    def __init__(self):
        self.api = KucoinAPI()
        self.data_manager = DataManager()
        self.model = TradingModel()
        self.risk_manager = RiskManager()
        self.scaler = MinMaxScaler()
        self.symbols = []
        self.timeframes = TRADE_TIMEFRAMES
        self.feature_columns = []  # Verrà popolato dalla feature selection
        self.all_features = []     # Elenco completo delle caratteristiche disponibili

        # Esegui la prima selezione delle coppie all'avvio
        self.select_best_pairs()

        # Pianifica la rivalutazione ogni 60 minuti e il reset giornaliero del drawdown
        schedule.every(60).minutes.do(self.select_best_pairs)
        schedule.every().day.at("00:00").do(self.risk_manager.reset_daily_drawdown)

    def select_best_pairs(self):
        print("Selezione delle migliori coppie USDT per lo scalping...")
        try:
            usdt_pairs = self.api.get_usdt_pairs()
            scores = []
            for ticker in usdt_pairs:
                symbol = ticker['symbol']
                vol_value = float(ticker['volValue'])
                if vol_value < MIN_VOLUME:
                    continue
                change_rate = abs(float(ticker['changeRate']))
                bid = float(ticker['buy'])
                ask = float(ticker['sell'])
                spread = ask - bid
                spread_percentage = (spread / bid) * 100 if bid > 0 else float('inf')
                if spread_percentage > MAX_SPREAD_PERCENTAGE:
                    continue
                score = (vol_value * change_rate) / spread_percentage
                scores.append({'symbol': symbol, 'score': score})
            top_pairs = sorted(scores, key=lambda x: x['score'], reverse=True)[:NUM_TOP_PAIRS]
            self.symbols = [pair['symbol'] for pair in top_pairs]
            print(f"Coppie selezionate: {self.symbols}")
        except Exception as e:
            print(f"Errore durante la selezione delle coppie: {e}")

    def feature_selection(self, X, y):
        print("Eseguendo la Feature Selection...")
        rf = RandomForestRegressor(n_estimators=100, random_state=42)
        rf.fit(X, y)
        importances = rf.feature_importances_
        feature_importance = pd.Series(importances, index=self.all_features)
        feature_importance = feature_importance.sort_values(ascending=False)
        N = 10  # Numero di caratteristiche da selezionare
        self.feature_columns = feature_importance.index[:N].tolist()
        print(f"Caratteristiche selezionate: {self.feature_columns}")
        input_dim = len(self.feature_columns)
        if os.path.exists(self.model.model_path):
            os.remove(self.model.model_path)
        self.model.build_model(input_dim)

    def prepare_data(self, data_frame):
        self.all_features = data_frame.columns.drop(['close', 'timestamp']).tolist()
        features = data_frame[self.all_features]
        target = data_frame['close']
        X_values = features.values
        y_values = target.values
        return X_values, y_values

    def trade_symbol(self, symbol, timeframe):
        try:
            market_data = self.api.get_historical_data(symbol, timeframe, limit=CANDLE_LIMIT)
            data_frame = pd.DataFrame(market_data)
            data_frame = calculate_indicators(data_frame)
            data_frame.dropna(inplace=True)
            if data_frame.empty:
                print(f"Dati insufficienti per {symbol} su timeframe {timeframe}.")
                return
            X, y = self.prepare_data(data_frame)
            if not self.feature_columns:
                self.feature_selection(X, y)
            X = data_frame[self.feature_columns].values
            X = X.reshape((X.shape[0], 1, X.shape[1]))
            X_scaled = self.scaler.fit_transform(X.reshape(-1, X.shape[-1])).reshape(X.shape)
            if not os.path.exists(self.model.model_path):
                print("Modello non trovato. Avvio dell'addestramento.")
                X_train, X_val, y_train, y_val = self.train_test_split(X_scaled, y)
                self.model.train(X_train, y_train, X_val, y_val)
            prediction = self.model.predict(X_scaled[-1].reshape(1, 1, -1))
            prediction = prediction[0][0]
            account_overview = self.api.get_account_overview()
            account_balance = float(account_overview.get('available', 0))
            atr = data_frame['atr'].iloc[-1]
            price = data_frame['close'].iloc[-1]
            position_size = self.risk_manager.calculate_position_size(account_balance, atr, price)
            if self.risk_manager.check_daily_drawdown(account_balance):
                self.make_decision(symbol, prediction, position_size, price)
        except Exception as e:
            print(f"Errore nel trading su {symbol} con timeframe {timeframe}: {e}")

    def make_decision(self, symbol, prediction, position_size, price):
        buy_threshold = 0.5
        sell_threshold = -0.5
        if prediction > buy_threshold:
            side = 'buy'
        elif prediction < sell_threshold:
            side = 'sell'
        else:
            print(f"Nessuna opportunità di trading per {symbol}. Prediction: {prediction}")
            return
        self.execute_trade(symbol, side, position_size, price)

    def execute_trade(self, symbol, side, amount, price):
        response = self.api.place_order(symbol, side, str(amount))
        if not PAPER_TRADING and response.get('orderId'):
            executed_price = price  # Usa il prezzo attuale se non sono forniti dettagli
            profit_loss = 0         # Impostato a zero; in futuro potresti calcolare il profitto/perdita
            self.data_manager.store_trade(symbol, side, amount, executed_price, profit_loss)
            print(f"Eseguito ordine {side} per {amount} {symbol} a {executed_price}")
        else:
            print(f"Ordine di test {side} per {amount} {symbol} eseguito.")

    def train_test_split(self, X, y, test_size=0.2):
        split_index = int(len(X) * (1 - test_size))
        X_train, X_val = X[:split_index], X[split_index:]
        y_train, y_val = y[:split_index], y[split_index:]
        return X_train, X_val, y_train, y_val

    def run(self):
        while True:
            schedule.run_pending()
            for symbol in self.symbols:
                for timeframe in self.timeframes:
                    self.trade_symbol(symbol, timeframe)
            time.sleep(1)
