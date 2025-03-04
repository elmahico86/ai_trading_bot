# test.py

import unittest
from src.trading_api import KucoinAPI
from src.bot import TradingBot

class TestKucoinAPI(unittest.TestCase):
    def setUp(self):
        self.api = KucoinAPI()

    def test_get_market_data(self):
        data = self.api.get_market_data('BTC-USDT')
        self.assertIsNotNone(data)
        self.assertIn('price', data)

    def test_place_order(self):
        # Test valido solo in modalità Paper Trading
        if PAPER_TRADING:
            response = self.api.place_order('BTC-USDT', 'buy', '0.001')
            self.assertIsNotNone(response)
        else:
            self.skipTest('Test valido solo in modalità Paper Trading')

class TestTradingBot(unittest.TestCase):
    def setUp(self):
        self.bot = TradingBot()

    def test_run(self):
        # Assicurarsi che il metodo run non generi eccezioni
        try:
            self.bot.run()
        except Exception as e:
            self.fail(f"Il metodo run() ha generato un'eccezione: {e}")

if __name__ == '__main__':
    unittest.main()
