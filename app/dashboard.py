import streamlit as st
import plotly.graph_objects as go

from app.market import calculate_indicators, fetch_history, latest_snapshot


st.set_page_config(page_title="StockSense Dashboard", page_icon="📈", layout="wide")
st.title("📈 StockSense — Real-Time Stock Market Dashboard")
st.caption("Market-data dashboard for analysis and decision support; not investment advice.")

symbol = st.sidebar.text_input("Stock symbol", "AAPL").strip().upper()
period = st.sidebar.selectbox("History", ["5d", "1mo", "3mo", "6mo", "1y", "2y"], index=1)
interval = st.sidebar.selectbox("Interval", ["1d", "1h", "30m", "15m", "5m"], index=0)

if st.sidebar.button("Refresh"):
    st.cache_data.clear()

try:
    df = calculate_indicators(fetch_history(symbol, period, interval))
    snap = latest_snapshot(df)

    c1, c2, c3 = st.columns(3)
    c1.metric("Price", f"{snap['price']:.2f}", f"{snap['change']:.2f} ({snap['change_pct']:.2f}%)")
    c2.metric("Volume", f"{snap['volume']:,}")
    c3.metric(
        "RSI (14)",
        f"{df['rsi_14'].dropna().iloc[-1]:.2f}" if df["rsi_14"].notna().any() else "N/A",
    )

    fig = go.Figure(
        data=[
            go.Candlestick(
                x=df.iloc[:, 0],
                open=df["open"],
                high=df["high"],
                low=df["low"],
                close=df["close"],
            )
        ]
    )
    fig.update_layout(title=f"{symbol} Price", xaxis_rangeslider_visible=False, height=550)
    st.plotly_chart(fig, use_container_width=True)

    st.subheader("Trend indicators")
    trend = go.Figure()
    trend.add_trace(go.Scatter(x=df.iloc[:, 0], y=df["close"], name="Close"))
    trend.add_trace(go.Scatter(x=df.iloc[:, 0], y=df["sma_20"], name="SMA 20"))
    trend.add_trace(go.Scatter(x=df.iloc[:, 0], y=df["sma_50"], name="SMA 50"))
    trend.update_layout(height=400)
    st.plotly_chart(trend, use_container_width=True)

    st.subheader("Latest data")
    st.dataframe(df.tail(20), use_container_width=True)
except Exception as exc:
    st.error(f"Unable to load {symbol}: {exc}")
