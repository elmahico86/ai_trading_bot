# switch.py

from src.config import PAPER_TRADING

def switch_paper_trading(state):
    with open('src/config.py', 'r') as file:
        lines = file.readlines()

    with open('src/config.py', 'w') as file:
        for line in lines:
            if line.strip().startswith('PAPER_TRADING'):
                file.write(f'PAPER_TRADING = {state}\n')
            else:
                file.write(line)
    print(f"Modalità Paper Trading {'attivata' if state else 'disattivata'}. Riavvia il bot per applicare le modifiche.")
