import pandas as pd
import yfinance as yf


def calculate_rsi(close_prices, period=14):
    delta = close_prices.diff()

    gain = delta.clip(lower=0)
    loss = -delta.clip(upper=0)

    avg_gain = gain.ewm(alpha=1/period, min_periods=period).mean()
    avg_loss = loss.ewm(alpha=1/period, min_periods=period).mean()

    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))

    return rsi


def calculate_market_signals(tickers):
    signals = []

    for ticker in tickers:
        stock = yf.Ticker(ticker)
        history = stock.history(period="1y")

        if history.empty:
            continue

        close_prices = history["Close"]

        current_price = close_prices.iloc[-1]

        rsi_series = calculate_rsi(close_prices)
        rsi = rsi_series.iloc[-1]

        if rsi > 70:
            rsi_signal = "Overbought"
        elif rsi < 30:
            rsi_signal = "Oversold"
        else:
            rsi_signal = "Neutral"

        ma20 = close_prices.tail(20).mean()
        ma50 = close_prices.tail(50).mean()

        trend = "Bullish" if ma20 > ma50 else "Bearish"

        difference_pct = (ma20 - ma50) / ma50 * 100

        signals.append({
            "Ticker": ticker,
            "Current Price": current_price,
            "MA20": ma20,
            "MA50": ma50,
            "Trend": trend,
            "MA_diff_pct": difference_pct,
            "RSI": rsi,
            "RSI Signal": rsi_signal
        })

    return pd.DataFrame(signals)