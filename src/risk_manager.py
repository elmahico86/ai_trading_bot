# risk_manager.py

class RiskManager:
    def __init__(self, max_risk_per_trade=0.01, max_daily_drawdown=0.05):
        self.max_risk_per_trade = max_risk_per_trade
        self.max_daily_drawdown = max_daily_drawdown
        self.daily_loss = 0

    def calculate_position_size(self, account_balance, stop_loss_pips, price):
        risk_amount = account_balance * self.max_risk_per_trade
        position_size = risk_amount / (stop_loss_pips * price)
        return position_size

    def update_daily_loss(self, loss):
        self.daily_loss += loss

    def check_daily_drawdown(self, account_balance):
        if self.daily_loss >= account_balance * self.max_daily_drawdown:
            print("Limite di perdita giornaliera raggiunto. Interrompo le operazioni per oggi.")
            return False
        return True

    def reset_daily_loss(self):
        self.daily_loss = 0
