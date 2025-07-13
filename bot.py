import requests
import time
import os
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

API_KEY = os.getenv("UNUSUAL_WHALES_API_KEY")
API_URL = "https://unusualwhales.com/api/historic_chains"

# === Filter Rules ===
MIN_DAYS_TO_EXPIRY = 30
MIN_AVERAGE_PRICE = 5
MIN_PREMIUM = 100_000

def fetch_alerts():
    headers = {"Authorization": f"Bearer {API_KEY}"}
    response = requests.get(API_URL, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        print("Failed to fetch data:", response.status_code)
        return []

def filter_alerts(alerts):
    valid_alerts = []
    for alert in alerts:
        try:
            expiry = datetime.strptime(alert['expiration'], "%Y-%m-%d")
            days_to_expiry = (expiry - datetime.now()).days
            avg_price = float(alert['average_price'])
            premium = float(alert['premium'])

            if (
                days_to_expiry >= MIN_DAYS_TO_EXPIRY and
                avg_price >= MIN_AVERAGE_PRICE and
                premium >= MIN_PREMIUM
            ):
                valid_alerts.append(alert)
        except Exception as e:
            continue
    return valid_alerts

def main():
    print("🔄 Starting alert scanner...")
    while True:
        alerts = fetch_alerts()
        trades = filter_alerts(alerts)
        for trade in trades:
            print(f"✅ {trade['ticker']} | {trade['side']} | Strike: {trade['strike']} | Exp: {trade['expiration']} | Premium: ${trade['premium']}")
            # 🔁 Here you will add the IBKR trade execution
        time.sleep(60)  # check every 1 min

if __name__ == "__main__":
    main()

    
# This script fetches options alerts from Unusual Whales, filters them based on defined rules,
# and prints valid trades. It runs in a loop, checking for new alerts every minute.
# You can extend it to execute trades using IBKR API.