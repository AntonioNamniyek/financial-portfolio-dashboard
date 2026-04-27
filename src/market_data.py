import yfinance as yf
import streamlit as st


@st.cache_data(ttl=300)
def get_current_prices(tickers):
    prices = []

    for ticker in tickers:
        try:
            stock = yf.Ticker(ticker)
            history = stock.history(period="5d")

            if history.empty or history["Close"].dropna().empty:
                prices.append(None)
            else:
                price = history["Close"].dropna().iloc[-1]
                prices.append(price)

        except Exception:
            prices.append(None)

    return prices