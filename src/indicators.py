import pandas as pd
import numpy as np

def calculate_indicators(data):
    data['sma'] = data['close'].rolling(window=14).mean()
    data['ema'] = data['close'].ewm(span=14, adjust=False).mean()
    data['rsi'] = calculate_rsi(data)
    data['macd'], data['macd_signal'], data['macd_hist'] = calculate_macd(data)
    data['adx'] = calculate_adx(data)
    data = calculate_ichimoku(data)
    data['bollinger_upper'], data['bollinger_lower'] = calculate_bollinger_bands(data)
    data['stochastic_k'], data['stochastic_d'] = calculate_stochastic_oscillator(data)
    data['atr'] = calculate_atr(data)
    data['momentum'] = calculate_momentum(data)
    data['vwap'] = calculate_vwap(data)
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

def calculate_macd(data, fast_period=12, slow_period=26, signal_period=9):
    exp1 = data['close'].ewm(span=fast_period, adjust=False).mean()
    exp2 = data['close'].ewm(span=slow_period, adjust=False).mean()
    macd = exp1 - exp2
    signal = macd.ewm(span=signal_period, adjust=False).mean()
    hist = macd - signal
    return macd, signal, hist

def calculate_adx(data, period=14):
    delta_high = data['high'].diff()
    delta_low = data['low'].diff()
    plus_dm = np.where((delta_high > delta_low) & (delta_high > 0), delta_high, 0)
    minus_dm = np.where((delta_low > delta_high) & (delta_low > 0), delta_low, 0)
    tr = calculate_true_range(data)
    plus_di = 100 * (pd.Series(plus_dm).rolling(window=period).sum() / pd.Series(tr).rolling(window=period).sum())
    minus_di = 100 * (pd.Series(minus_dm).rolling(window=period).sum() / pd.Series(tr).rolling(window=period).sum())
    dx = (abs(plus_di - minus_di) / (plus_di + minus_di)) * 100
    adx = dx.rolling(window=period).mean()
    return adx

def calculate_true_range(data):
    data['h_l'] = data['high'] - data['low']
    data['h_c'] = abs(data['high'] - data['close'].shift())
    data['l_c'] = abs(data['low'] - data['close'].shift())
    tr = data[['h_l', 'h_c', 'l_c']].max(axis=1)
    return tr

def calculate_ichimoku(data):
    high9 = data['high'].rolling(window=9).max()
    low9 = data['low'].rolling(window=9).min()
    data['tenkan_sen'] = (high9 + low9) / 2
    high26 = data['high'].rolling(window=26).max()
    low26 = data['low'].rolling(window=26).min()
    data['kijun_sen'] = (high26 + low26) / 2
    data['senkou_span_a'] = ((data['tenkan_sen'] + data['kijun_sen']) / 2).shift(26)
    high52 = data['high'].rolling(window=52).max()
    low52 = data['low'].rolling(window=52).min()
    data['senkou_span_b'] = ((high52 + low52) / 2).shift(26)
    data['chikou_span'] = data['close'].shift(-26)
    return data

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

def calculate_momentum(data, period=10):
    momentum = data['close'] - data['close'].shift(period)
    return momentum

def calculate_vwap(data):
    q = data['volume']
    p = data['close']
    vwap = (p * q).cumsum() / q.cumsum()
    return vwap
