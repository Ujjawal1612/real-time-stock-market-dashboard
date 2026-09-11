# 📈 StockSense — Real-Time Stock Market Dashboard

A Python-based stock-market dashboard for near-real-time market-data monitoring, historical analysis, technical indicators, and API access.

## Features

- Stock symbol search
- Current price, daily change, and volume
- Historical market data through Yahoo Finance
- Candlestick charts
- SMA 20 / SMA 50
- RSI 14
- MACD and signal line
- FastAPI REST API
- Streamlit dashboard
- Docker support
- Automated tests with GitHub Actions

## Architecture

```text
Yahoo Finance → market.py → FastAPI / Streamlit
                         └→ indicators → charts & metrics
```

## Run locally

```bash
python -m venv .venv

# Windows
.venv\Scripts\activate

# macOS/Linux
source .venv/bin/activate

pip install -r requirements.txt
streamlit run app/dashboard.py
```

API:

```bash
uvicorn app.api:app --reload
```

Then open `/docs` on the API server for interactive documentation.

## Tests

```bash
pytest -q
```

## Docker

```bash
docker build -t stocksense .
docker run --rm -p 8501:8501 stocksense
```

## Data note

Market data is retrieved from Yahoo Finance through `yfinance`. Availability and update frequency depend on the upstream data source and selected interval. This project is for educational and analytical use and does not provide personalized investment advice.
