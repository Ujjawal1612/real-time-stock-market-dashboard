import os


def explain_market(symbol, snapshot, indicators, prediction):
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        return "LLM explanation is disabled. Add OPENAI_API_KEY to enable the market summary."

    from openai import OpenAI

    client = OpenAI(api_key=api_key)
    prompt = f"""
Explain this stock dashboard for an educational project. Do not give personalized investment advice.
Stock: {symbol}
Current price: {snapshot['price']:.2f}
Daily change: {snapshot['change_pct']:.2f}%
RSI: {indicators['rsi']:.2f}
SMA20: {indicators['sma20']:.2f}
SMA50: {indicators['sma50']:.2f}
MACD: {indicators['macd']:.4f}
ML next-close estimate: {prediction:.2f}

Give a short explanation with: current trend, technical indicators, and reasons the ML estimate could be wrong. Clearly say the ML estimate is experimental.
"""
    response = client.responses.create(model="gpt-5-mini", input=prompt)
    return response.output_text
