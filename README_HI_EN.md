# tradewithTushar — Indian Stock Research Prototype

## Features included
- Hindi/English interface
- Search for a ticker and download available Yahoo Finance history
- NSE default suffix (`.NS`) when no exchange suffix is entered; enter `.BO` for BSE or a global ticker explicitly
- Candlestick chart with EMA20, EMA50 and volume
- RSI, MACD, ATR-based illustrative entry/stop/targets
- Google News RSS headline search
- 1,000-path bootstrap simulation from historical daily returns
- Basic EMA20/EMA50 crossover historical test

## Important limits
This is a research/education prototype, not an autonomous trading system. It does not connect to a broker or place orders. Yahoo Finance may be delayed, incomplete, rate-limited, or lack intraday coverage. Google News RSS is not a guaranteed complete breaking-news feed. Technical labels are rule-based, not an AI guarantee. The simulation is not a prediction and the risk slider is not yet used for position sizing. Test strategies out-of-sample and include transaction costs before relying on results.

## Run locally
Python 3.10+ recommended.

```bash
pip install -r requirements.txt
streamlit run app.py
```

## Deploy free (if available to your account)
1. Create a GitHub repository and upload `app.py` and `requirements.txt`.
2. In Streamlit Community Cloud, create an app from that repository and choose `app.py`.
3. Public apps and service limits depend on Streamlit's current terms. Do not put API secrets in the code or a public repository.

## Symbol examples
- `RELIANCE.NS`
- `TCS.NS`
- `HDFCBANK.NS`
- `INFY.NS`
- `^NSEI` (Nifty 50 index)
- `^BSESN` (Sensex)
- `AAPL` (US ticker)

If a symbol doesn't return data, check the provider's supported symbol and exchange suffix.
