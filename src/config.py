# config.py

import os
from dotenv import load_dotenv

# Carica le variabili d'ambiente dal file .env
load_dotenv()

# Chiavi API di KuCoin
API_KEY = os.getenv('KUCOIN_API_KEY')
API_SECRET = os.getenv('KUCOIN_API_SECRET')
API_PASSPHRASE = os.getenv('KUCOIN_API_PASSPHRASE')

# Impostazioni di trading
PAPER_TRADING = True  # Modalità Paper Trading attiva per default

# Parametri di trading
SYMBOL = 'BTC-USDT'
TRADE_AMOUNT = 0.001

# Altre configurazioni
LOG_FILE = 'ai_trading_bot.log'
