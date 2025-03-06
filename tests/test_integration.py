import unittest
import os
import pandas as pd
import numpy as np
from unittest.mock import patch, MagicMock
from src.bot import TradingBot
from src.trading_api import KucoinAPI
from src.config import NUM_TOP_PAIRS, TRADE_TIMEFRAMES
from src.indicators import calculate_indicators


class TestTradingSystem(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.bot = TradingBot()
        cls.bot.api.client = MagicMock()  # Mock the KuCoin client

    def setUp(self):
        # Reset mocks before each test
        self.bot.api.client.get_kline_data.reset_mock()
        self.bot.api.client.get_ticker.reset_mock()

    def tearDown(self):
        # Cleanup residual files if any
        model_path = 'models/test_model.h5'
        if os.path.exists(model_path):
            os.remove(model_path)

    def test_1_api_connectivity(self):
        """Verifica la connessione all'API e la selezione delle coppie"""
        # Mock API response
        mock_tickers = [{'symbol': f'TEST{i}-USDT', 'volValue': 2000000,
                         'buy': 1.0, 'sell': 1.001, 'changeRate': 0.05}
                        for i in range(10)]
        self.bot.api.client.get_all_tickers.return_value = {'data': {'ticker': mock_tickers}}

        self.bot.select_best_pairs()
        self.assertEqual(len(self.bot.symbols), NUM_TOP_PAIRS)
        print("Test 1 superato: Selezione coppie funzionante")

    def test_2_historical_data_fetch(self):
        """Verifica il recupero dei dati storici"""
        # Mock historical data
        mock_data = [[1600000000, 1.0, 1.1, 1.2, 0.9, 1000]] * 1000
        self.bot.api.client.get_kline_data.return_value = mock_data

        data = self.bot.api.get_historical_data('TEST-USDT', '1min', limit=1000)
        self.assertEqual(len(data), 1000)
        print("Test 2 superato: Recupero dati storici funzionante")

    def test_3_data_preprocessing(self):
        """Verifica il preprocessing dei dati e il calcolo degli indicatori"""
        test_data = pd.DataFrame({
            'open': np.random.rand(100),
            'high': np.random.rand(100),
            'low': np.random.rand(100),
            'close': np.random.rand(100),
            'volume': np.random.rand(100)
        })
        processed_data = calculate_indicators(test_data)
        self.assertIn('rsi', processed_data.columns)
        self.assertFalse(processed_data.isnull().values.any())
        print("Test 3 superato: Preprocessing dati corretto")

    def test_4_model_training(self):
        """Verifica l'addestramento del modello"""
        # Generate dummy data
        X_train = np.random.rand(100, 1, 10)
        y_train = np.random.rand(100)

        # Build and train model
        model_path = 'models/test_model.h5'
        self.bot.model.model_path = model_path
        self.bot.model.build_model(10)
        history = self.bot.model.train(X_train, y_train, X_train, y_train)

        self.assertTrue(os.path.exists(model_path))
        self.assertIn('loss', history.history)
        print("Test 4 superato: Addestramento modello funzionante")

    def test_5_paper_trading(self):
        """Verifica l'esecuzione degli ordini in paper trading"""
        self.bot.api.client._request.return_value = {'orderId': 'test123'}

        self.bot.api.paper_trading = True
        response = self.bot.api.place_order('TEST-USDT', 'buy', 0.1)
        self.assertIn('orderId', response)
        print("Test 5 superato: Paper trading funzionante")

    def test_6_insufficient_data(self):
        """Verifica la gestione di dati insufficienti"""
        self.bot.api.client.get_kline_data.return_value = []

        data = self.bot.api.get_historical_data('TEST-USDT', '1min', limit=100)
        self.assertEqual(len(data), 0)
        print("Test 6 superato: Dati insufficienti gestiti correttamente")


@unittest.skip("Test reali non inclusi per questa esecuzione")
class TestRealAPI(unittest.TestCase):
    def test_7_real_api_connection(self):
        """Verifica la connessione reale all'API di KuCoin"""
        try:
            # Usa l'API reale (senza mocking)
            tickers = self.bot.api.get_all_tickers()
            self.assertIsInstance(tickers, list)
            self.assertGreater(len(tickers), 0)
            print("Test 7 superato: Connessione API reale funzionante")
        except Exception as e:
            self.fail(f"Errore nella connessione API reale: {e}")

    def test_8_real_historical_data(self):
        """Verifica il recupero di dati storici reali"""
        try:
            # Usa l'API reale
            data = self.bot.api.get_historical_data('BTC-USDT', '1min', limit=10)
            self.assertIsInstance(data, list)
            self.assertEqual(len(data), 10)
            print("Test 8 superato: Recupero dati storici reali funzionante")
        except Exception as e:
            self.fail(f"Errore nel recupero dati storici reali: {e}")


if __name__ == '__main__':
    unittest.main(verbosity=2)
