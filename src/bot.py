# src/bot.py

import asyncio
from data_manager import DataManager
from model import TradingModel
from trading_api import TradingAPI
from risk_manager import RiskManager
from alert_system import AlertSystem
from config import SYMBOLS, RISK_PARAMS, TIME_INTERVALS
from indicators import calculate_atr

class TradingBot:
    def __init__(self):
        self.data_manager = DataManager()
        self.model = TradingModel()
        self.trading_api = TradingAPI()
        self.risk_manager = RiskManager(RISK_PARAMS['initial_balance'])
        self.alert_system = AlertSystem()
        self.symbols = SYMBOLS

    async def run(self):
        await self.model.load()
        while True:
            tasks = [self.process_symbol(symbol) for symbol in self.symbols]
            await asyncio.gather(*tasks)
            await asyncio.sleep(TIME_INTERVALS['tick_processing'])

    async def process_symbol(self, symbol):
        data = self.data_manager.get_latest_data(symbol)
        data = self.data_manager.preprocess_data(data)
        if data.empty or len(data) < TIME_STEPS:
            return
        X = self.prepare_input(data)
        prediction = self.model.predict(X)
        decision = self.should_trade(data, prediction)
        if decision in ['buy', 'sell']:
            await self.execute_trade(symbol, decision, data)

    def prepare_input(self, data):
        features = data.tail(TIME_STEPS).drop(['timestamp', 'symbol'], axis=1).values
        features = features.reshape(1, TIME_STEPS, -1)
        return features

    def should_trade(self, data, prediction):
        # Logica decisionale avanzata
        # Esempio semplificato:
        if prediction > 0.5:
            return 'buy'
        elif prediction < -0.5:
            return 'sell'
        else:
            return 'hold'

    async def execute_trade(self, symbol, decision, data):
        atr = calculate_atr(data)
        current_price = data['close'].iloc[-1]
        position = await self.trading_api.get_position(symbol)
        
        if decision == 'buy' and not position:
            stop_loss = self.risk_manager.calculate_stop_loss(current_price, atr)
            take_profit = self.risk_manager.calculate_take_profit(current_price, atr)
            qty = self.risk_manager.calculate_position_size(RISK_PARAMS['risk_per_trade'], current_price - stop_loss)
            order = await self.trading_api.place_order(symbol, qty, 'buy')
            self.alert_system.send_message(f"Aperta posizione LONG su {symbol} con quantità {qty}")
        elif decision == 'sell' and position:
            order = await self.trading_api.place_order(symbol, position['qty'], 'sell')
            self.alert_system.send_message(f"Chiusa posizione su {symbol}")
        else:
            pass  # Nessuna azione

    async def stop(self):
        await self.data_manager.close()
        await self.trading_api.close()
