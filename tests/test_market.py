import pandas as pd

from app.market import calculate_indicators, latest_snapshot


def sample():
    return pd.DataFrame(
        {
            "Date": pd.date_range("2025-01-01", periods=60),
            "open": range(100, 160),
            "high": range(101, 161),
            "low": range(99, 159),
            "close": range(100, 160),
            "volume": [1000] * 60,
        }
    )


def test_indicators_and_snapshot():
    df = calculate_indicators(sample())
    assert "sma_20" in df and "rsi_14" in df and "macd" in df

    snap = latest_snapshot(df)
    assert snap["price"] == 159.0
    assert snap["change"] == 1.0
