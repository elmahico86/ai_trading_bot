# src/config.py

import os
from dotenv import load_dotenv
import tensorflow as tf

load_dotenv()

# API Keys e Configurazioni
API_KEY = os.getenv('API_KEY')
API_SECRET = os.getenv('API_SECRET')
ENVIRONMENT = os.getenv('ENVIRONMENT', 'paper')

# Configurazione della GPU
MAX_GPU_MEMORY_MB = int(0.85 * 8192)  # 85% di 8GB di memoria GPU
gpus = tf.config.experimental.list_physical_devices('GPU')
if gpus:
    try:
        tf.config.experimental.set_virtual_device_configuration(
            gpus[0],
            [tf.config.experimental.VirtualDeviceConfiguration(memory_limit=MAX_GPU_MEMORY_MB)]
        )
        logical_gpus = tf.config.experimental.list_logical_devices('GPU')
        print(f"{len(gpus)} GPU fisica, {len(logical_gpus)} GPU logica.")
    except RuntimeError as e:
        print(e)

# Percorsi dei file
DATABASE_PATH = 'data/trading_data.db'
MODEL_PATH = 'models/trading_model.keras'
SCALER_PATH = 'models/scaler.pkl'

# Parametri del modello
TIME_STEPS = 60
N_FEATURES = 80

# Parametri di trading
RISK_PARAMS = {
    'initial_balance': 100000,
    'risk_per_trade': 0.01
}

# Parametri di mercato
SYMBOLS = ['EURUSD', 'GBPUSD', 'USDJPY', 'AUDUSD']

# Parametri del bot
TIME_INTERVALS = {
    'data_fetch': 60,  # in secondi
    'model_train': 3600,  # in secondi
    'tick_processing': 1  # in secondi
}

# Configurazioni per Telegram
TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
TELEGRAM_CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')
