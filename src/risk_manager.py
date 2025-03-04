# src/risk_manager.py

class RiskManager:
    def __init__(self, initial_balance, base_risk=0.01, atr_multiplier=2):
        self.account_balance = initial_balance
        self.base_risk = base_risk
        self.atr_multiplier = atr_multiplier

    def calculate_stop_loss(self, entry_price, atr):
        stop_loss = entry_price - (atr * self.atr_multiplier)
        return stop_loss

    def calculate_take_profit(self, entry_price, atr):
        take_profit = entry_price + (atr * self.atr_multiplier)
        return take_profit

    def calculate_position_size(self, risk_per_trade, stop_loss_pips):
        risk_amount = self.account_balance * risk_per_trade
        position_size = risk_amount / stop_loss_pips
        return position_size

    def update_account_balance(self, profit_loss):
        self.account_balance += profit_loss
