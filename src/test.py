# src/test.py

import unittest
from data_manager import DataManager
from model import TradingModel
import pandas as pd

class TestTradingBot(unittest.TestCase):
    def setUp(self):
        self.data_manager = DataManager()
        self.model = TradingModel()

    def test_data_fetch(self):
        df = self.data_manager.get_latest_data('EURUSD')
        self.assertIsNotNone(df)
        self.assertGreater(len(df), 0)

    def test_model_prediction(self):
        df = pd.read_csv('test_data.csv')
        df = self.data_manager.preprocess_data(df)
        X = df.drop(['timestamp', 'symbol'], axis=1).values.reshape(1, TIME_STEPS, -1)
        prediction = self.model.predict(X)
        self.assertIsNotNone(prediction)

    def tearDown(self):
        pass

if __name__ == '__main__':
    unittest.main()
