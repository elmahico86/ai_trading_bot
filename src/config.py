# config.py

import os
from dotenv import load_dotenv

load_dotenv()

# Chiavi API di KuCoin
API_KEY = os.getenv('KUCOIN_API_KEY')
API_SECRET = os.getenv('KUCOIN_API_SECRET')
API_PASSPHRASE = os.getenv('KUCOIN_API_PASSPHRASE')

# Impostazioni di trading
PAPER_TRADING = True  # Modalità Paper Trading attiva di default

# Parametri di trading
TRADE_SYMBOLS = ['BTC-USDT', 'ETH-USDT', 'ADA-USDT']  # Coppie ottimizzate
TRADE_TIMEFRAMES = ['1min', '5min', '15min']  # Timeframe per lo scalping
MAX_RISK_PER_TRADE = 0.01  # 1% del capitale per trade
MAX_DAILY_DRAWDOWN = 0.05  # 5% di perdita massima giornaliera

# Altre configurazioni
LOG_FILE = 'ai_trading_bot.log'
