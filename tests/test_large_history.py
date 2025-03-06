from src.trading_api import KucoinAPI

def test_get_large_history():
    """
    Test per verificare la funzionalità di get_large_history.
    Recupera 1000 candele per BTC-USDT con timeframe 1min.
    """
    api = KucoinAPI()
    symbol = 'BTC-USDT'
    timeframe = '1min'
    total_limit = 1000

    try:
        # Recupera le candele usando il metodo get_large_history
        candles = api.get_large_history(symbol, timeframe, total_limit)

        # Stampa il risultato del test
        print(f"Numero di candele recuperate: {len(candles)}")
        if len(candles) == total_limit:
            print("Test superato: numero di candele corretto.")
        elif len(candles) < total_limit:
            print(f"Test parzialmente superato: numero di candele recuperate {len(candles)}. "
                  f"Non ci sono abbastanza dati disponibili.")
        else:
            print("Test fallito: sono state recuperate troppe candele.")

        # Verifica che i dati siano cronologicamente ordinati
        timestamps = [candle[0] for candle in candles]  # Accesso al timestamp con indice 0
        assert timestamps == sorted(timestamps), "Errore: Le candele non sono ordinate cronologicamente."
        print("Le candele sono correttamente ordinate.")

    except Exception as e:
        print(f"Errore durante il test: {e}")

if __name__ == "__main__":
    test_get_large_history()
