# indicators.py

import pandas as pd

def calculate_indicators(data):
    data['sma'] = data['close'].rolling(window=14).mean()
    data['ema'] = data['close'].ewm(span=14, adjust=False).mean()
    data['rsi'] = calculate_rsi(data)
    data['bollinger_upper'], data['bollinger_lower'] = calculate_bollinger_bands(data)
    data['stochastic_k'], data['stochastic_d'] = calculate_stochastic_oscillator(data)
    data['atr'] = calculate_atr(data)
    return data

def calculate_rsi(data, periods=14):
    delta = data['close'].diff()
    gain = (delta.where(delta > 0, 0)).fillna(0)
    loss = (-delta.where(delta < 0, 0)).fillna(0)
    avg_gain = gain.rolling(window=periods).mean()
    avg_loss = loss.rolling(window=periods).mean()
    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))
    return rsi

def calculate_bollinger_bands(data, window=20, num_std=2):
    rolling_mean = data['close'].rolling(window).mean()
    rolling_std = data['close'].rolling(window).std()
    upper_band = rolling_mean + (rolling_std * num_std)
    lower_band = rolling_mean - (rolling_std * num_std)
    return upper_band, lower_band

def calculate_stochastic_oscillator(data, period=14):
    low_min = data['low'].rolling(window=period).min()
    high_max = data['high'].rolling(window=period).max()
    stochastic_k = 100 * (data['close'] - low_min) / (high_max - low_min)
    stochastic_d = stochastic_k.rolling(window=3).mean()
    return stochastic_k, stochastic_d

def calculate_atr(data, period=14):
    data['tr'] = data[['high', 'close']].max(axis=1) - data[['low', 'close']].min(axis=1)
    atr = data['tr'].rolling(window=period).mean()
    return atr
