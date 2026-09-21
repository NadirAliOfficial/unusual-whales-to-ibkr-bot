import requests
import time
import os
from dotenv import load_dotenv
from ib_insync import IB, Stock, MarketOrder, LimitOrder

load_dotenv()

API_KEY = os.getenv("UNUSUAL_WHALES_API_KEY")
TWS_HOST = os.getenv("TWS_HOST", "127.0.0.1")
TWS_PORT = int(os.getenv("TWS_PORT", 7497))
TWS_CLIENT_ID = int(os.getenv("TWS_CLIENT_ID", 1))
DRY_RUN = os.getenv("DRY_RUN", "false").lower() == "true"

# === Filter Rules ===
MIN_VOLUME = int(os.getenv("MIN_VOLUME", 500_000))
MIN_PRICE = float(os.getenv("MIN_PRICE", 5.0))
MIN_DOLLAR_VOLUME = float(os.getenv("MIN_DOLLAR_VOLUME", 5_000_000))
ORDER_TYPE = os.getenv("ORDER_TYPE", "MKT")
SHARES_PER_TRADE = int(os.getenv("SHARES_PER_TRADE", 100))

HEADERS = {"Authorization": f"Bearer {API_KEY}"}
SEEN = set()


def fetch_flow():
    url = "https://api.unusualwhales.com/api/screener/stocks"
    params = {"limit": 50, "order": "desc", "order_by": "relative_volume"}
    resp = requests.get(url, headers=HEADERS, params=params, timeout=10)
    if resp.status_code == 200:
        return resp.json().get("data", [])
    print(f"API error: {resp.status_code}")
    return []


def filter_alerts(alerts):
    valid = []
    for a in alerts:
        try:
            ticker = a.get("ticker", "").upper()
            volume = int(a.get("volume", 0))
            price = float(a.get("close", a.get("last_price", 0)))
            dollar_vol = volume * price

            if ticker in SEEN:
                continue
            if volume < MIN_VOLUME:
                continue
            if price < MIN_PRICE:
                continue
            if dollar_vol < MIN_DOLLAR_VOLUME:
                continue

            valid.append({"ticker": ticker, "price": price, "volume": volume, "dollar_vol": dollar_vol})
        except Exception:
            continue
    return valid


def place_order(ib, alert):
    contract = Stock(alert["ticker"], "SMART", "USD")
    ib.qualifyContracts(contract)

    if ORDER_TYPE == "LMT":
        order = LimitOrder("BUY", SHARES_PER_TRADE, round(alert["price"] * 1.001, 2))
    else:
        order = MarketOrder("BUY", SHARES_PER_TRADE)

    if DRY_RUN:
        print(f"[DRY RUN] Would buy {SHARES_PER_TRADE} {alert['ticker']} @ {ORDER_TYPE}")
        return

    trade = ib.placeOrder(contract, order)
    print(f"Order placed: {SHARES_PER_TRADE} {alert['ticker']} | {ORDER_TYPE} | ${alert['price']:.2f} | Vol: {alert['volume']:,}")
    return trade


def connect_ibkr():
    ib = IB()
    ib.connect(TWS_HOST, TWS_PORT, clientId=TWS_CLIENT_ID)
    return ib


def main():
    print(f"Starting Unusual Whales stock flow bot (DRY_RUN={DRY_RUN})")
    ib = connect_ibkr()

    while True:
        try:
            alerts = fetch_flow()
            targets = filter_alerts(alerts)

            for alert in targets:
                place_order(ib, alert)
                SEEN.add(alert["ticker"])

            if not targets:
                print(f"No qualifying alerts — checked {len(alerts)} tickers")

        except Exception as e:
            print(f"Error: {e}")
            try:
                ib.disconnect()
                ib = connect_ibkr()
            except Exception:
                pass

        time.sleep(60)


if __name__ == "__main__":
    main()
