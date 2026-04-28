import yfinance as yf
import streamlit as st


def normalize_ticker(ticker):
    ticker = str(ticker).upper().strip()

    if ticker.startswith("^"):
        return ticker

    if "-" in ticker:
        return ticker

    if ticker.endswith("USD") and len(ticker) > 3:
        return ticker[:-3] + "-USD"

    return ticker


@st.cache_data(ttl=300)
def get_current_prices(tickers):
    prices = []

    for ticker in tickers:
        try:
            yf_ticker = normalize_ticker(ticker)

            stock = yf.Ticker(yf_ticker)
            history = stock.history(period="5d")

            if history.empty or history["Close"].dropna().empty:
                prices.append(None)
            else:
                price = history["Close"].dropna().iloc[-1]
                prices.append(price)

        except Exception:
            prices.append(None)

    return prices