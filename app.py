from datetime import datetime

import streamlit as st

from src.data_loader import load_selected_portfolio
from src.portfolio import calculate_portfolio_values, calculate_totals
from src.market_data import get_current_prices
from src.charts import create_allocation_chart, create_pnl_chart, create_ma_diff_chart
from src.formatting import prepare_display_table, style_display_table
from src.indicators import calculate_market_signals
from src.ui import apply_custom_layout, render_header, render_metrics


apply_custom_layout()

render_header(datetime.now().strftime("%d/%m/%Y %H:%M"))

df = load_selected_portfolio()
df["current_price"] = get_current_prices(df["ticker"])
df = calculate_portfolio_values(df)

selected_tickers = st.multiselect(
    "Select assets",
    options=df["ticker"].unique(),
    default=df["ticker"].unique()
)

if not selected_tickers:
    st.warning("Please select at least one asset.")
    st.stop()

df_filtered = df[df["ticker"].isin(selected_tickers)]

total_invested, total_current_value, total_pnl, total_pnl_percentage = calculate_totals(df_filtered)
render_metrics(total_invested, total_current_value, total_pnl, total_pnl_percentage)

st.divider()

st.subheader("Portfolio")

df_display = prepare_display_table(df_filtered)
styled_df = style_display_table(df_display)

st.dataframe(styled_df, width="stretch")

st.divider()

st.subheader("Portfolio Insights")

chart_col1, chart_col2 = st.columns(2)

with chart_col1:
    fig_allocation = create_allocation_chart(df_filtered)
    fig_allocation.update_layout(height=400)
    st.plotly_chart(fig_allocation, width="stretch")

with chart_col2:
    fig_pnl = create_pnl_chart(df_filtered)
    fig_pnl.update_layout(height=400)
    st.plotly_chart(fig_pnl, width="stretch")

st.divider()

st.subheader("Market Signals")

signals_df = calculate_market_signals(df_filtered["ticker"])

fig_ma = create_ma_diff_chart(signals_df)
fig_ma.update_layout(height=400)
st.plotly_chart(fig_ma, width="stretch")

signals_df["MA20"] = signals_df["MA20"].map(lambda x: f"${x:,.2f}")
signals_df["MA50"] = signals_df["MA50"].map(lambda x: f"${x:,.2f}")
signals_df["MA_diff_pct"] = signals_df["MA_diff_pct"].map(lambda x: f"{x:.2f}%")
signals_df["RSI"] = signals_df["RSI"].map(lambda x: f"{x:.2f}")

signals_df = signals_df.rename(columns={
    "MA_diff_pct": "MA: Percentage difference"
})

st.dataframe(signals_df, width="stretch")