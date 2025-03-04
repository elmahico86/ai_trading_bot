# bot.py

import pandas as pd
import numpy as np
import schedule
import time
import os
from sklearn.preprocessing import MinMaxScaler
from src.trading_api import KucoinAPI
from src.data_manager import DataManager
from src.indicators import calculate_indicators
from src.model import TradingModel
from src.risk_manager import RiskManager
from src.config import NUM_TOP_PAIRS, TRADE_TIMEFRAMES, PAPER_TRADING, MIN_VOLUME, MAX_SPREAD_PERCENTAGE

class TradingBot:
    def __init__(self):
        self.api = KucoinAPI()
        self.data_manager = DataManager()
        self.model = TradingModel()
        self.risk_manager = RiskManager()
        self.scaler = MinMaxScaler()
        self.symbols = []
        self.timeframes = TRADE_TIMEFRAMES

        # Esegui la prima selezione all'avvio
        self.select_best_pairs()

        # Pianifica la rivalutazione ogni 60 minuti
        schedule.every(60).minutes.do(self.select_best_pairs)
        schedule.every().day.at("00:00").do(self.risk_manager.reset_daily_loss)

    def select_best_pairs(self):
        print("Selezione delle migliori coppie USDT per lo scalping...")
        try:
            usdt_pairs = self.api.get_usdt_pairs()
            scores = []

            for ticker in usdt_pairs:
                symbol = ticker['symbol']
                vol_value = float(ticker['volValue'])
                if vol_value < MIN_VOLUME:
                    continue  # Esclude coppie con volume inferiore al minimo

                change_rate = abs(float(ticker['changeRate']))
                bid = float(ticker['buy'])
                ask = float(ticker['sell'])
                spread = ask - bid
                spread_percentage = (spread / bid) * 100 if bid > 0 else float('inf')

                if spread_percentage > MAX_SPREAD_PERCENTAGE:
                    continue  # Esclude coppie con spread superiore al massimo

                # Calcola il punteggio
                score = (vol_value * change_rate) / spread_percentage
                scores.append({'symbol': symbol, 'score': score})

            # Ordina per punteggio decrescente e seleziona le top N coppie
            top_pairs = sorted(scores, key=lambda x: x['score'], reverse=True)[:NUM_TOP_PAIRS]
            self.symbols = [pair['symbol'] for pair in top_pairs]
            print(f"Coppie selezionate: {self.symbols}")
        except Exception as e:
            print(f"Errore durante la selezione delle coppie: {e}")

    def run(self):
        while True:
            # Esegui le attività pianificate
            schedule.run_pending()
            for symbol in self.symbols:
                for timeframe in self.timeframes:
                    self.trade_symbol(symbol, timeframe)
            time.sleep(1)  # Attendi 1 secondo prima del prossimo ciclo

    def trade_symbol(self, symbol, timeframe):
        try:
            # Recupera dati storici
            market_data = self.api.get_historical_data(symbol, timeframe, limit=100)
            data_frame = pd.DataFrame(market_data)
            data_frame = calculate_indicators(data_frame)
            data_frame.dropna(inplace=True)

            if data_frame.empty:
                print(f"Dati insufficienti per {symbol} su timeframe {timeframe}.")
                return

            # Prepara i dati per il modello
            X, y = self.prepare_data(data_frame)

            # Normalizza le caratteristiche
            X_scaled = self.scaler.fit_transform(X)

            # Addestra o carica il modello
            if not os.path.exists(self.model.model_path):
                print("Modello non trovato. Avvio dell'addestramento.")
                X_train, X_val, y_train, y_val = self.train_test_split(X_scaled, y)
                self.model.train(X_train, y_train, X_val, y_val)

            # Effettua la previsione
            prediction = self.model.predict(X_scaled[-1].reshape(1, -1))
            prediction = prediction[0][0]

            # Gestione del rischio
            account_balance = float(self.api.get_account_overview()['availableBalance'])
            atr = data_frame['atr'].iloc[-1]
            price = data_frame['close'].iloc[-1]
            position_size = self.risk_manager.calculate_position_size(account_balance, atr, price)

            # Decisione di trading
            if self.risk_manager.check_daily_drawdown(account_balance):
                self.make_decision(symbol, prediction, position_size, price)
        except Exception as e:
            print(f"Errore nel trading su {symbol} con timeframe {timeframe}: {e}")

    def prepare_data(self, data_frame):
        features = data_frame.drop(['close', 'timestamp'], axis=1)
        target = data_frame['close']
        return features.values, target.values

    def train_test_split(self, X, y, test_size=0.2):
        split_index = int(len(X) * (1 - test_size))
        X_train, X_val = X[:split_index], X[split_index:]
        y_train, y_val = y[:split_index], y[split_index:]
        return X_train, X_val, y_train, y_val

    def make_decision(self, symbol, prediction, position_size, price):
        # Threshold per la decisione
        buy_threshold = 0.5
        sell_threshold = -0.5

        if prediction > buy_threshold:
            side = 'buy'
        elif prediction < sell_threshold:
            side = 'sell'
        else:
            print(f"Nessuna opportunità di trading per {symbol}. Prediction: {prediction}")
            return

        # Esegue il trade
        self.execute_trade(symbol, side, position_size, price)

    def execute_trade(self, symbol, side, amount, price):
        response = self.api.place_order(symbol, side, str(amount))
        if not PAPER_TRADING and response.get('orderId'):
            executed_price = price  # In assenza di informazioni dettagliate, usiamo il prezzo attuale
            profit_loss = 0  # Calcolo del profitto/perdita da implementare
            self.data_manager.store_trade(symbol, side, amount, executed_price, profit_loss)
            print(f"Eseguito ordine {side} per {amount} {symbol} a {executed_price}")
        else:
            print(f"Ordine di test {side} per {amount} {symbol} eseguito.")

    def reset_daily_loss(self):
        self.risk_manager.reset_daily_loss()
        print("Perdita giornaliera resettata.")

