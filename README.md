# Unusual Whales to IBKR Stock Bot

A Python bot that monitors unusual stock activity from the [Unusual Whales API](https://unusualwhales.com), filters by volume and price criteria, and automatically executes stock buy orders through Interactive Brokers (IBKR).

---

## Features

- Polls Unusual Whales screener for high relative-volume stock alerts
- Filters by minimum volume, price, and dollar volume thresholds
- Executes market or limit buy orders via `ib_insync`
- Deduplicates tickers within a session — won't re-enter the same stock twice
- Dry-run mode for testing filters without submitting orders
- Auto-reconnects to TWS on connection drop
- All config via `.env` — no hardcoded values

---

## Requirements

- Python 3.8+
- IBKR TWS or IB Gateway running locally
- Active Unusual Whales API key

```bash
pip install requests python-dotenv ib_insync
```

---

## .env Setup

```env
UNUSUAL_WHALES_API_KEY=your_key_here
TWS_HOST=127.0.0.1
TWS_PORT=7497
TWS_CLIENT_ID=1

# Filter thresholds
MIN_VOLUME=500000
MIN_PRICE=5.0
MIN_DOLLAR_VOLUME=5000000

# Order config
ORDER_TYPE=MKT        # MKT or LMT
SHARES_PER_TRADE=100

# Set to true to log orders without submitting
DRY_RUN=false
```

---

## Run

```bash
python bot.py
```

Polls every 60 seconds. Qualifying tickers are logged and orders are placed immediately. Duplicate tickers within the same session are skipped.

---

## How It Works

1. Fetches the top 50 stocks by relative volume from Unusual Whales screener
2. Applies filters: volume ≥ MIN_VOLUME, price ≥ MIN_PRICE, dollar volume ≥ MIN_DOLLAR_VOLUME
3. Qualifies each ticker as a SMART-routed US equity contract via IBKR
4. Places a market or limit buy order for SHARES_PER_TRADE shares
5. Marks ticker as seen — won't trade it again until bot restarts

---

## License

MIT
