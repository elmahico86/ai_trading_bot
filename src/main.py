# main.py

from src.bot import TradingBot
from src.config import SYMBOL, TRADE_AMOUNT

def main():
    bot = TradingBot()
    bot.run(SYMBOL, TRADE_AMOUNT)

if __name__ == '__main__':
    main()
