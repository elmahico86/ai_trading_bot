# test.py

import unittest
from src.trading_api import KucoinAPI

class TestKucoinAPI(unittest.TestCase):
    def setUp(self):
        self.api = KucoinAPI()

    def test_get_market_data(self):
        data = self.api.get_market_data('BTC-USDT')
        self.assertIsNotNone(data)
        self.assertIn('price', data)

    def test_place_order(self):
        # Questo test sarà valido solo in modalità Paper Trading
        if self.api.client.url == 'https://openapi-sandbox.kucoin.com':
            order = self.api.place_order('BTC-USDT', 'buy', '0.001')
            self.assertIsNotNone(order)
            self.assertIn('orderId', order)
        else:
            self.skipTest('Test valido solo in modalità Paper Trading')

if __name__ == '__main__':
    unittest.main()
