# src/main.py

import asyncio
from bot import TradingBot
import logging
import logging.config
import json

def setup_logging():
    with open('logging_config.json', 'r') as f:
        config_dict = json.load(f)
    logging.config.dictConfig(config_dict)

if __name__ == '__main__':
    setup_logging()
    bot = TradingBot()
    try:
        asyncio.run(bot.run())
    except KeyboardInterrupt:
        print("Bot interrotto dall'utente.")
        asyncio.run(bot.stop())
