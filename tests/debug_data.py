from src.trading_api import KucoinAPI

api = KucoinAPI()
symbol = 'BTC-USDT'  # Cambia con altre coppie per test
timeframes = ['1min', '5min', '15min']

for timeframe in timeframes:
    data = api.get_large_history(symbol, timeframe, total_limit=1000)
    print(f"Timeframe {timeframe}: {len(data)} candele recuperate.")
