import yfinance as yf
import streamlit as st

@st.cache_data
def get_current_prices(tickers):
    prices = []

    for ticker in tickers:
        try:
            stock = yf.Ticker(ticker)
            price = stock.history(period="1d")["Close"].iloc[-1]
        except:
            price = None  # fallback se der erro

        prices.append(price)

    return prices