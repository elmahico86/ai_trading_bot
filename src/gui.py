# gui.py

import tkinter as tk
from tkinter import ttk
from threading import Thread
from src.bot import TradingBot
from src.config import PAPER_TRADING

class TradingBotGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("AI Trading Bot")
        self.paper_trading = PAPER_TRADING
        self.bot = TradingBot()

        self.create_widgets()

    def create_widgets(self):
        # Frame principale
        main_frame = tk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Switch Paper Trading
        self.switch_var = tk.BooleanVar(value=self.paper_trading)
        self.switch_button = tk.Checkbutton(
            main_frame, text="Modalità Paper Trading",
            variable=self.switch_var, command=self.toggle_paper_trading
        )
        self.switch_button.pack(anchor=tk.W)

        # Avvia Bot
        self.start_button = tk.Button(main_frame, text="Avvia Bot", command=self.start_bot)
        self.start_button.pack(anchor=tk.W)

        # Barra di progresso
        self.progress = ttk.Progressbar(main_frame, orient='horizontal', length=300, mode='determinate')
        self.progress.pack(pady=10)

        # ETA Label
        self.eta_label = tk.Label(main_frame, text="Tempo stimato: --:--")
        self.eta_label.pack()

        # Log Text
        self.log_text = tk.Text(main_frame, height=15)
        self.log_text.pack(fill=tk.BOTH, expand=True)

    def toggle_paper_trading(self):
        self.paper_trading = self.switch_var.get()
        # Aggiorna la configurazione
        self.bot.paper_trading = self.paper_trading

    def start_bot(self):
        # Avvia il bot in un thread separato
        thread = Thread(target=self.run_bot)
        thread.start()

    def run_bot(self):
        # Simula operazioni che richiedono tempo con avanzamento
        total_steps = 100  # Supponiamo
        for i in range(total_steps):
            # Aggiorna la barra di progresso
            self.progress['value'] = (i + 1) / total_steps * 100
            self.root.update_idletasks()
            # Aggiorna ETA
            eta = self.calculate_eta(i + 1, total_steps)
            self.eta_label.config(text=f"Tempo stimato: {eta}")
            # Log
            self.log_text.insert(tk.END, f"Esecuzione step {i + 1}/{total_steps}\n")
            # Simula tempo di elaborazione
            time.sleep(0.1)

        # Esegui il bot vero e proprio
        self.bot.run()

    def calculate_eta(self, current_step, total_steps):
        # Calcola un ETA fittizio
        remaining = total_steps - current_step
        eta_seconds = remaining * 0.1  # Tempo per step simulato
        minutes, seconds = divmod(eta_seconds, 60)
        return f"{int(minutes):02d}:{int(seconds):02d}"

if __name__ == '__main__':
    root = tk.Tk()
    app = TradingBotGUI(root)
    root.mainloop()
