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
NUM_TOP_PAIRS = 5  # Numero di migliori coppie USDT da selezionare
TRADE_TIMEFRAMES = ['1min', '5min', '15min']  # Timeframes per lo scalping

MAX_RISK_PER_TRADE = 0.01  # 1% del capitale per trade
MAX_DAILY_DRAWDOWN = 0.05  # 5% di perdita massima giornaliera
MIN_VOLUME = 1000000  # Volume minimo in USDT per considerare una coppia
MAX_SPREAD_PERCENTAGE = 0.1  # Spread massimo come percentuale del prezzo (0.1%)

# Altre configurazioni
LOG_FILE = 'ai_trading_bot.log'
