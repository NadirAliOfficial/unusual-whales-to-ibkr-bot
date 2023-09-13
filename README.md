
# Unusual Whales to IBKR Trading Bot

This Python bot fetches real-time options flow alerts from the [Unusual Whales Public API](https://unusualwhales.com/public-api), filters them based on your custom rules, and prepares them for automated trading through Interactive Brokers (IBKR).

---

## ✅ Features

- Real-time options flow data from Unusual Whales
- Custom filters:
  - Expiry ≥ 30 days
  - Average fill ≥ $5
  - Premium ≥ $100,000
- Easy-to-modify filtering logic
- Modular structure ready for IBKR order execution

---

## 📦 Requirements

- Python 3.8+
- `requests`
- `python-dotenv`
- An active Unusual Whales API key
- IBKR TWS or IB Gateway running (for integration)

Install dependencies:
```bash
pip install -r requirements.txt
````

---

## 🔐 .env Setup

Create a `.env` file in the root directory:

```
UNUSUAL_WHALES_API_KEY=your_api_key_here
```

---

## 🚀 Run the Bot

```bash
python bot.py
```

The bot will scan alerts every 60 seconds, apply your filters, and print trade-ready alerts.

---

## 🛠 To-Do (Next Steps)

* [ ] Integrate IBKR via `ib_insync`
* [ ] Add Discord/Webhook notifications
* [ ] Optional: Web UI to control filters
* [ ] Docker deployment

---

## 📄 License

MIT License — Free for personal and commercial use.
<!-- updated: 2023-09-13-r01 -->
