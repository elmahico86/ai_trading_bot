# gui.py

import tkinter as tk
from src.config import PAPER_TRADING
from src.switch import switch_paper_trading
from src.main import main

class TradingBotGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("AI Trading Bot")
        self.paper_trading = PAPER_TRADING

        self.create_widgets()

    def create_widgets(self):
        self.switch_button = tk.Button(self.root, text="Modalità Paper Trading: ON" if self.paper_trading else "Modalità Paper Trading: OFF", command=self.toggle_paper_trading)
        self.switch_button.pack()

        self.start_button = tk.Button(self.root, text="Avvia Bot", command=main)
        self.start_button.pack()

    def toggle_paper_trading(self):
        self.paper_trading = not self.paper_trading
        switch_paper_trading(self.paper_trading)
        stato = "ON" if self.paper_trading else "OFF"
        self.switch_button.config(text=f"Modalità Paper Trading: {stato}")

if __name__ == '__main__':
    root = tk.Tk()
    app = TradingBotGUI(root)
    root.mainloop()
