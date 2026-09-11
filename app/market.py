from __future__ import annotations

import pandas as pd


def fetch_history(symbol: str, period: str = "1mo", interval: str = "1d") -> pd.DataFrame:
    symbol = symbol.strip().upper()
    if not symbol:
        raise ValueError("Stock symbol cannot be empty")

    # Imported lazily so the offline analysis functions remain usable without yfinance.
    import yfinance as yf

    df = yf.download(symbol, period=period, interval=interval, auto_adjust=False, progress=False)
    if df.empty:
        raise ValueError(f"No market data found for {symbol}")

    if isinstance(df.columns, pd.MultiIndex):
        df.columns = df.columns.get_level_values(0)
    df.columns = [str(c).lower().replace(" ", "_") for c in df.columns]
    return df.reset_index()


def calculate_indicators(df: pd.DataFrame) -> pd.DataFrame:
    out = df.copy()
    close = out["close"]

    out["sma_20"] = close.rolling(20).mean()
    out["sma_50"] = close.rolling(50).mean()

    delta = close.diff()
    gain = delta.clip(lower=0).rolling(14).mean()
    loss = -delta.clip(upper=0).rolling(14).mean()
    rs = gain / loss.replace(0, pd.NA)
    out["rsi_14"] = 100 - (100 / (1 + rs))

    ema12 = close.ewm(span=12, adjust=False).mean()
    ema26 = close.ewm(span=26, adjust=False).mean()
    out["macd"] = ema12 - ema26
    out["macd_signal"] = out["macd"].ewm(span=9, adjust=False).mean()
    return out


def latest_snapshot(df: pd.DataFrame) -> dict:
    valid = df.dropna(subset=["close"])
    row = valid.iloc[-1]
    previous = valid.iloc[-2] if len(valid) > 1 else row

    close = float(row["close"])
    prev = float(previous["close"])
    change = close - prev

    return {
        "price": close,
        "change": change,
        "change_pct": (change / prev * 100) if prev else 0.0,
        "volume": int(row["volume"]) if pd.notna(row.get("volume")) else 0,
    }
