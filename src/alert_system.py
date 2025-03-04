# src/alert_system.py

import requests
from config import TELEGRAM_TOKEN, TELEGRAM_CHAT_ID

class AlertSystem:
    def __init__(self):
        self.token = TELEGRAM_TOKEN
        self.chat_id = TELEGRAM_CHAT_ID

    def send_message(self, text):
        url = f"https://api.telegram.org/bot{self.token}/sendMessage"
        params = {'chat_id': self.chat_id, 'text': text}
        requests.post(url, params=params)
