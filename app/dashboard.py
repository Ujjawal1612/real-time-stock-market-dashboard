import streamlit as st
import plotly.graph_objects as go

from app.market import calculate_indicators, fetch_history, latest_snapshot

st.set_page_config(page_title="StockSense", page_icon="📈", layout="wide")

st.title("📈 StockSense")
st.write("Simple stock market dashboard for checking price history and technical indicators.")
st.caption("For learning and analysis only. This is not investment advice.")

symbol = st.sidebar.text_input("Enter stock symbol", "AAPL").upper().strip()
period = st.sidebar.selectbox(
    "Select time period", ["5d", "1mo", "3mo", "6mo", "1y", "2y"]
)
interval = st.sidebar.selectbox(
    "Select interval", ["1d", "1h", "30m", "15m", "5m"]
)

if st.sidebar.button("Refresh data"):
    st.rerun()

if not symbol:
    st.warning("Please enter a stock symbol.")
    st.stop()

try:
    data = fetch_history(symbol, period, interval)
    data = calculate_indicators(data)
    latest = latest_snapshot(data)

    col1, col2, col3 = st.columns(3)
    col1.metric("Current price", f"{latest['price']:.2f}")
    col2.metric(
        "Change",
        f"{latest['change']:.2f}",
        f"{latest['change_pct']:.2f}%",
    )
    col3.metric("Volume", f"{latest['volume']:,}")

    st.subheader(f"{symbol} price chart")

    price_chart = go.Figure()
    price_chart.add_trace(
        go.Candlestick(
            x=data.iloc[:, 0],
            open=data["open"],
            high=data["high"],
            low=data["low"],
            close=data["close"],
            name=symbol,
        )
    )
    price_chart.update_layout(xaxis_rangeslider_visible=False, height=500)
    st.plotly_chart(price_chart, use_container_width=True)

    st.subheader("Moving averages")

    trend_chart = go.Figure()
    trend_chart.add_trace(
        go.Scatter(x=data.iloc[:, 0], y=data["close"], name="Close")
    )
    trend_chart.add_trace(
        go.Scatter(x=data.iloc[:, 0], y=data["sma_20"], name="SMA 20")
    )
    trend_chart.add_trace(
        go.Scatter(x=data.iloc[:, 0], y=data["sma_50"], name="SMA 50")
    )
    trend_chart.update_layout(height=400)
    st.plotly_chart(trend_chart, use_container_width=True)

    st.subheader("RSI and MACD")

    rsi = data.dropna(subset=["rsi_14"])
    if not rsi.empty:
        rsi_chart = go.Figure()
        rsi_chart.add_trace(go.Scatter(x=rsi.iloc[:, 0], y=rsi["rsi_14"], name="RSI"))
        rsi_chart.add_hline(y=70, line_dash="dash")
        rsi_chart.add_hline(y=30, line_dash="dash")
        rsi_chart.update_layout(height=300)
        st.plotly_chart(rsi_chart, use_container_width=True)

    macd_chart = go.Figure()
    macd_chart.add_trace(go.Scatter(x=data.iloc[:, 0], y=data["macd"], name="MACD"))
    macd_chart.add_trace(
        go.Scatter(x=data.iloc[:, 0], y=data["macd_signal"], name="Signal")
    )
    macd_chart.update_layout(height=300)
    st.plotly_chart(macd_chart, use_container_width=True)

    st.subheader("Recent data")
    st.dataframe(data.tail(20), use_container_width=True)

except Exception as e:
    st.error(f"Could not load data for {symbol}: {e}")
