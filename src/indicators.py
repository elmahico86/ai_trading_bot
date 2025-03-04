# indicators.py

import pandas as pd

def calculate_sma(data, window):
    return data['close'].rolling(window=window).mean()

def calculate_ema(data, window):
    return data['close'].ewm(span=window, adjust=False).mean()

def calculate_rsi(data, periods=14):
    delta = data['close'].diff(1)
    gain = delta.where(delta > 0, 0)
    loss = -delta.where(delta < 0, 0)
    avg_gain = gain.ewm(com=(periods - 1), min_periods=periods).mean()
    avg_loss = loss.ewm(com=(periods - 1), min_periods=periods).mean()
    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))
    return rsi
