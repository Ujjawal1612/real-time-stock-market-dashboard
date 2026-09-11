from fastapi import FastAPI, HTTPException, Query

from .market import calculate_indicators, fetch_history, latest_snapshot

app = FastAPI(title="Stock Market Dashboard API", version="1.0.0")


@app.get("/")
def root():
    return {"name": "Stock Market Dashboard API", "status": "ok"}


@app.get("/health")
def health():
    return {"status": "healthy"}


@app.get("/stocks/{symbol}")
def stock(
    symbol: str,
    period: str = Query("1mo"),
    interval: str = Query("1d"),
):
    try:
        df = calculate_indicators(fetch_history(symbol, period, interval))
        data = df.tail(100).copy()
        data = data.where(data.notna(), None)
        if not data.empty:
            data.iloc[:, 0] = data.iloc[:, 0].astype(str)
        return {
            "symbol": symbol.strip().upper(),
            "snapshot": latest_snapshot(df),
            "data": data.to_dict("records"),
        }
    except Exception as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
