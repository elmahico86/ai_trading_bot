# test.py

import unittest
from src.trading_api import KucoinAPI
from src.bot import TradingBot
from src.config import PAPER_TRADING

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
            print("Test ordine di test eseguito correttamente.")
        else:
            self.skipTest('Test valido solo in modalità Paper Trading')

    def test_get_usdt_pairs(self):
        pairs = self.api.get_usdt_pairs()
        self.assertTrue(len(pairs) > 0)
        print(f"Numero di coppie USDT recuperate: {len(pairs)}")

class TestTradingBot(unittest.TestCase):
    def setUp(self):
        self.bot = TradingBot()

    def test_select_best_pairs(self):
        self.bot.select_best_pairs()
        self.assertTrue(len(self.bot.symbols) > 0)
        print(f"Coppie selezionate per il trading: {self.bot.symbols}")

    def test_run(self):
        # Questo test esegue solo una singola iterazione per verificare che il bot funzioni senza errori
        try:
            self.bot.run()
        except Exception as e:
            self.fail(f"Il metodo run() ha generato un'eccezione: {e}")

if __name__ == '__main__':
    unittest.main()
