# src/indicators.py

import pandas as pd
import numpy as np
from functools import lru_cache

def compute_indicators(df):
    df = df.copy()
    
    # RSI
    delta = df['close'].diff()
    gain = np.where(delta > 0, delta, 0)
    loss = np.where(delta < 0, -delta, 0)
    avg_gain = pd.Series(gain).rolling(window=14).mean()
    avg_loss = pd.Series(loss).rolling(window=14).mean()
    rs = avg_gain / avg_loss
    df['RSI'] = 100 - (100 / (1 + rs))
    
    # MACD
    ema12 = df['close'].ewm(span=12, adjust=False).mean()
    ema26 = df['close'].ewm(span=26, adjust=False).mean()
    df['MACD'] = ema12 - ema26
    df['Signal'] = df['MACD'].ewm(span=9, adjust=False).mean()
    
    # Bollinger Bands
    sma = df['close'].rolling(window=20).mean()
    std = df['close'].rolling(window=20).std()
    df['Bollinger_Upper'] = sma + (std * 2)
    df['Bollinger_Lower'] = sma - (std * 2)
    
    # Altri indicatori possono essere aggiunti qui
    
    return df

@lru_cache(maxsize=None)
def calculate_atr(df):
    df = df.copy()
    df['H-L'] = df['high'] - df['low']
    df['H-C'] = np.abs(df['high'] - df['close'].shift())
    df['L-C'] = np.abs(df['low'] - df['close'].shift())
    df['TR'] = df[['H-L', 'H-C', 'L-C']].max(axis=1)
    atr = df['TR'].rolling(window=14).mean()
    return atr.iloc[-1]
