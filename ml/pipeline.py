import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

FEATURES = ["return_1d", "return_5d", "sma_20_gap", "sma_50_gap", "rsi_14", "macd"]


def make_features(data):
    df = data.copy()
    df["return_1d"] = df["close"].pct_change()
    df["return_5d"] = df["close"].pct_change(5)
    df["sma_20"] = df["close"].rolling(20).mean()
    df["sma_50"] = df["close"].rolling(50).mean()
    df["sma_20_gap"] = (df["close"] - df["sma_20"]) / df["sma_20"]
    df["sma_50_gap"] = (df["close"] - df["sma_50"]) / df["sma_50"]

    change = df["close"].diff()
    gain = change.clip(lower=0).rolling(14).mean()
    loss = -change.clip(upper=0).rolling(14).mean()
    rs = gain / loss.replace(0, pd.NA)
    df["rsi_14"] = 100 - (100 / (1 + rs))

    ema12 = df["close"].ewm(span=12, adjust=False).mean()
    ema26 = df["close"].ewm(span=26, adjust=False).mean()
    df["macd"] = ema12 - ema26
    df["target"] = df["close"].shift(-1)
    return df


def train_model(data):
    df = make_features(data).dropna().copy()
    if len(df) < 60:
        raise ValueError("At least 60 rows are needed to train the model.")

    split = int(len(df) * 0.8)
    train = df.iloc[:split]
    test = df.iloc[split:]

    model = Pipeline([
        ("scale", StandardScaler()),
        ("model", RandomForestRegressor(
            n_estimators=150, max_depth=8, random_state=42
        )),
    ])
    model.fit(train[FEATURES], train["target"])
    predictions = model.predict(test[FEATURES])
    mae = mean_absolute_error(test["target"], predictions)
    next_price = float(model.predict(df.iloc[[-1]][FEATURES])[0])
    return model, next_price, float(mae)
