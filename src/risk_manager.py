# risk_manager.py

class RiskManager:
    def __init__(self, max_risk_per_trade=0.01, max_daily_drawdown=0.05):
        self.max_risk_per_trade = max_risk_per_trade
        self.max_daily_drawdown = max_daily_drawdown
        self.daily_loss = 0

    def calculate_position_size(self, prediction_confidence):
        # Calcola la dimensione della posizione in base al rischio
        available_capital = self.get_available_capital()
        risk_amount = available_capital * self.max_risk_per_trade
        position_size = risk_amount * prediction_confidence
        return position_size

    def update_daily_loss(self, loss):
        self.daily_loss += loss
        if self.daily_loss >= self.get_available_capital() * self.max_daily_drawdown:
            # Stop trading per il resto della giornata
            self.stop_trading()

    def get_available_capital(self):
        # Recupera il capitale disponibile
        account_info = self.api.client.get_account_overview()
        return float(account_info['available'])

    def stop_trading(self):
        print("Raggiunto il massimo drawdown giornaliero. Interrompo le operazioni.")
        exit()
