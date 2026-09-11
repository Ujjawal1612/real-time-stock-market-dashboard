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
- Offline runnable demo with sample data
- Docker support
- Automated tests with GitHub Actions

## Project structure
```text
real-time-stock-market-dashboard/
├── app/
│   ├── market.py          # Data fetching + indicators
│   ├── dashboard.py       # Streamlit UI
│   └── api.py             # FastAPI endpoints
├── data/
│   └── sample_stock_data.csv
├── notebooks/
│   └── StockSense_Demo.ipynb
├── tests/
│   └── test_market.py
├── .github/workflows/tests.yml
├── Dockerfile
├── requirements.txt
└── README.md
```

## Run the project
```bash
python -m venv .venv
# Windows
.venv\Scripts\activate
# macOS/Linux
source .venv/bin/activate
pip install -r requirements.txt
streamlit run app/dashboard.py
```

Open the displayed Streamlit URL, enter a ticker such as `AAPL`, and refresh to retrieve market data.

## Run the notebook and see results
Open `notebooks/StockSense_Demo.ipynb` in Jupyter Notebook or VS Code. It uses the included `data/sample_stock_data.csv`, so the analysis pipeline is runnable even without internet access.

The saved demo shows example results such as:
```text
Latest Price : 89.57
Change       : -3.22 (-3.47%)
Volume       : 1,345,977
RSI (14)     : 53.26
```

It also produces price/SMA and RSI charts.

## FastAPI
```bash
uvicorn app.api:app --reload
```
Then open `/docs` on the API server for interactive API documentation.

Example:
```text
GET /stocks/AAPL?period=1mo&interval=1d
```

## Tests
```bash
pytest -q
```

## Docker
```bash
docker build -t stocksense .
docker run --rm -p 8501:8501 stocksense
```

## Architecture
```text
Yahoo Finance → market.py → FastAPI / Streamlit
                         └→ indicators → metrics & charts

Sample CSV → market.py → Jupyter Demo → saved example results
```

## Data note
Market data is retrieved from Yahoo Finance through `yfinance`. Availability and update frequency depend on the upstream data source and selected interval. The project is for educational and analytical use and does not provide personalized investment advice.
