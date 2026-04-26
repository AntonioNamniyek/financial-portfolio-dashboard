import pandas as pd
import yfinance as yf


def calculate_rsi(close_prices, period=14):
    delta = close_prices.diff()

    gain = delta.clip(lower=0)
    loss = -delta.clip(upper=0)

    avg_gain = gain.rolling(period).mean()
    avg_loss = loss.rolling(period).mean()

    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))

    return rsi


def calculate_market_signals(tickers):
    signals = []

    for ticker in tickers:
        stock = yf.Ticker(ticker)
        history = stock.history(period="6mo")

        rsi_series = calculate_rsi(history["Close"])
        rsi = rsi_series.iloc[-1]

        if rsi > 70:
            rsi_signal = "Overbought"
        elif rsi < 30:
            rsi_signal = "Oversold"
        else:
            rsi_signal = "Neutral"

        ma20 = history["Close"].tail(20).mean()
        ma50 = history["Close"].tail(50).mean()

        trend = "Bullish" if ma20 > ma50 else "Bearish"

        difference_pct = (ma20 - ma50) / ma50 * 100

        signals.append({
            "Ticker": ticker,
            "MA20": ma20,
            "MA50": ma50,
            "Trend": trend,
            "MA_diff_pct": difference_pct,
            "RSI": rsi,
            "RSI Signal": rsi_signal
        })

    return pd.DataFrame(signals)