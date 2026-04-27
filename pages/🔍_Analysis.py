import streamlit as st

from src.ui import apply_custom_layout, render_signal_box
from src.tradingview import render_tradingview_chart
from src.indicators import calculate_market_signals


apply_custom_layout()


st.title("📈 Analysis")

st.caption("Search an asset and analyze price action, indicators and market signals.")

ticker_input = st.text_input(
    "Search ticker",
    placeholder="Example: AAPL, TSLA, NVDA, BTCUSD"
).upper()

yf_ticker = ticker_input
tv_ticker = ticker_input

if ticker_input in ["BTCUSD", "ETHUSD", "SOLUSD"]:
    yf_ticker = ticker_input.replace("USD", "-USD")
    tv_ticker = ticker_input

if ticker_input:
    signals_df = calculate_market_signals([yf_ticker])

    if signals_df.empty:
        st.error("Ticker not found or no market data available.")
        st.stop()

    signal = signals_df.iloc[0]

    col1, col2, col3, col4 = st.columns(4, gap="large")

    col1.metric("Current Price", f"${signal['Current Price']:,.2f}")
    col2.metric("MA20", f"${signal['MA20']:,.2f}")
    col3.metric("MA50", f"${signal['MA50']:,.2f}")
    col4.metric("RSI", f"{signal['RSI']:.2f}", signal["RSI Signal"])

    render_signal_box(
    signal["Trend"],
    signal["RSI"],
    signal["MA_diff_pct"]
)

    st.divider()

    st.markdown(f"### {ticker_input} Chart")

    render_tradingview_chart(tv_ticker)

else:
    st.info("Search for a ticker to start the analysis.")

