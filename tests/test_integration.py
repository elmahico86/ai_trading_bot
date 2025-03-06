import unittest
import os
import sys
import pandas as pd
import numpy as np
from unittest.mock import patch, MagicMock
from src.bot import TradingBot
from src.trading_api import KucoinAPI
from src.config import NUM_TOP_PAIRS, TRADE_TIMEFRAMES
from src.indicators import calculate_indicators

# Cambia la working directory alla root del progetto
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
os.chdir(project_root)
sys.path.insert(0, project_root)

class TestTradingSystem(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.bot = TradingBot()
        # Configura il client come MagicMock solo per i test mockati
        cls.bot.api.client = MagicMock()

    def setUp(self):
        # Resetta SOLO i mock utilizzati nei test specifici
        if hasattr(self.bot.api.client, 'get_kline_data'):
            self.bot.api.client.get_kline_data.reset_mock()
        if hasattr(self.bot.api.client, 'get_ticker'):
            self.bot.api.client.get_ticker.reset_mock()

    def tearDown(self):
        # Cleanup residual files if any
        model_path = 'models/test_model.h5'
        if os.path.exists(model_path):
            os.remove(model_path)

    # Test 1: Mockato
    def test_1_api_connectivity(self):
        """Verifica la connessione all'API e la selezione delle coppie"""
        # Configura il mock per get_all_tickers
        mock_tickers = [{'symbol': f'TEST{i}-USDT', 'volValue': 2000000, 'buy': 1.0, 'sell': 1.001, 'changeRate': 0.05} for i in range(10)]
        self.bot.api.client.get_all_tickers.return_value = {'data': {'ticker': mock_tickers}}

        self.bot.select_best_pairs()
        self.assertEqual(len(self.bot.symbols), NUM_TOP_PAIRS)
        print("Test 1 superato: Selezione coppie funzionante")

    # Test 2: Mockato
    def test_2_historical_data_fetch(self):
        """Verifica il recupero dei dati storici"""
        # Configura il mock per get_kline_data
        mock_data = [[1600000000, 1.0, 1.1, 1.2, 0.9, 1000]] * 1000
        self.bot.api.client.get_kline_data.return_value = mock_data

        data = self.bot.api.get_historical_data('TEST-USDT', '1min', limit=1000)
        self.assertEqual(len(data), 1000)
        print("Test 2 superato: Recupero dati storici funzionante")

    # Test 3: Non richiede mock
    def test_3_data_preprocessing(self):
        """Verifica il preprocessing dei dati e il calcolo degli indicatori"""
        test_data = pd.DataFrame({
            'open': np.random.rand(300),
            'high': np.random.rand(300),
            'low': np.random.rand(300),
            'close': np.random.rand(300),
            'volume': np.random.rand(300)
        })
        
        processed_data = calculate_indicators(test_data)
        processed_data.dropna(inplace=True)
        
        self.assertGreater(len(processed_data), 150)
        self.assertIn('rsi', processed_data.columns)
        print("Test 3 superato: Preprocessing dati corretto")

    # Test 4: Non richiede mock
    def test_4_model_training(self):
        """Verifica l'addestramento del modello"""
        X_train = np.random.rand(100, 1, 10)
        y_train = np.random.rand(100)
        model_path = 'models/test_model.h5'
        self.bot.model.model_path = model_path
        self.bot.model.build_model(10)
        history = self.bot.model.train(X_train, y_train, X_train, y_train)
        self.assertTrue(os.path.exists(model_path))
        self.assertIn('loss', history.history)
        print("Test 4 superato: Addestramento modello funzionante")

    # Test 5: Mockato
    @patch('src.trading_api.Client')
    def test_5_paper_trading(self, mock_client):
        """Verifica l'esecuzione degli ordini in paper trading"""
        mock_response = {'data': {'orderId': 'test123'}, 'code': '200000'}
        mock_client.return_value._request.return_value = mock_response

        self.bot.api.paper_trading = True
        response = self.bot.api.place_order('TEST-USDT', 'buy', 0.1)
        self.assertIn('orderId', response.get('data', {}))
        print("Test 5 superato: Paper trading funzionante")

    # Test 6-8: Test reali (senza mock)
    def test_6_real_api_connection(self):
        """Verifica la connessione reale all'API di KuCoin"""
        # Usa il client reale
        real_api = KucoinAPI()
        try:
            tickers = real_api.get_all_tickers()
            self.assertIsInstance(tickers, list)
            self.assertGreater(len(tickers), 0)
            print("Test 6 superato: Connessione API reale funzionante")
        except Exception as e:
            self.fail(f"Errore API: {e}")

    def test_7_real_historical_data(self):
        """Verifica il recupero di dati storici reali"""
        real_api = KucoinAPI()
        try:
            data = real_api.get_historical_data('BTC-USDT', '1min', limit=10)
            self.assertIsInstance(data, list)
            self.assertGreater(len(data), 0)
            print("Test 7 superato: Recupero dati storici reali funzionante")
        except Exception as e:
            self.fail(f"Errore dati storici: {e}")

    def test_8_real_historical_data(self):
        """Verifica il recupero di dati storici reali"""
        real_api = KucoinAPI()
        try:
            data = real_api.get_historical_data('BTC-USDT', '1min', limit=10)
            self.assertIsInstance(data, list)
            self.assertGreater(len(data), 0)
            print("Test 8 superato: Recupero dati storici reali funzionante")
        except Exception as e:
            self.fail(f"Errore nel recupero dati storici reali: {e}")

if __name__ == '__main__':
    unittest.main(verbosity=2)