# model.py

import numpy as np
from tensorflow.keras.models import load_model

class TradingModel:
    def __init__(self, model_path='models/trading_model.keras', scaler_path='models/scaler.pkl'):
        self.model = load_model(model_path)
        # Carica lo scaler se necessario

    def predict(self, data):
        # Effettua le previsioni sul set di dati fornito
        predictions = self.model.predict(data)
        return predictions
