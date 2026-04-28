import streamlit as st
import pandas as pd

from src.market_data import get_current_prices
from src.portfolio import (
    calculate_portfolio_values,
    calculate_totals,
    get_portfolio_history,
    calculate_portfolio_history,
    calculate_daily_pnl,
    get_benchmark_history,
    compare_with_benchmark
)
from src.formatting import prepare_display_table
from src.ui import render_metrics, apply_custom_layout
from src.charts import (
    create_allocation_chart,
    create_pnl_chart,
    create_portfolio_performance_chart,
)


apply_custom_layout()

st.title("💼 Portfolio")

if "portfolio" not in st.session_state:
    st.session_state.portfolio = pd.DataFrame(columns=[
        "ticker",
        "quantity",
        "buy_price",
        "buy_date"
    ])

with st.form("add_asset_form"):
    col1, col2 = st.columns(2, gap="large")

    with col1:
        ticker = st.text_input("Ticker").upper()
        quantity = st.number_input("Quantity", min_value=0.0)

    with col2:
        buy_price = st.number_input("Buy Price", min_value=0.0)
        buy_date = st.date_input("Buy Date")

    submitted = st.form_submit_button("➕ Add Asset")

    if submitted:
        if ticker == "" or quantity == 0 or buy_price == 0:
            st.warning("Please fill all fields correctly.")
        else:
            existing_asset = st.session_state.portfolio["ticker"] == ticker

            if existing_asset.any():
                asset_index = st.session_state.portfolio[existing_asset].index[0]

                old_quantity = st.session_state.portfolio.loc[asset_index, "quantity"]
                old_buy_price = st.session_state.portfolio.loc[asset_index, "buy_price"]

                old_invested = old_quantity * old_buy_price
                new_invested = quantity * buy_price

                new_quantity = old_quantity + quantity
                average_buy_price = (old_invested + new_invested) / new_quantity

                st.session_state.portfolio.loc[asset_index, "quantity"] = new_quantity
                st.session_state.portfolio.loc[asset_index, "buy_price"] = average_buy_price
                st.session_state.portfolio.loc[asset_index, "buy_date"] = buy_date

                st.success(f"{ticker} position updated!")
            else:
                new_row = pd.DataFrame([{
                    "ticker": ticker,
                    "quantity": quantity,
                    "buy_price": buy_price,
                    "buy_date": buy_date
                }])

                st.session_state.portfolio = pd.concat(
                    [st.session_state.portfolio, new_row],
                    ignore_index=True
                )

                st.success(f"{ticker} added to portfolio!")

            st.rerun()

if not st.session_state.portfolio.empty:
    df = st.session_state.portfolio.copy()

    df["current_price"] = get_current_prices(df["ticker"])
    df = calculate_portfolio_values(df)

    total_invested, total_current_value, total_pnl, total_pnl_percentage = calculate_totals(df)

    render_metrics(
        total_invested,
        total_current_value,
        total_pnl,
        total_pnl_percentage
    )

    st.divider()

    chart_col1, chart_col2 = st.columns([1, 1], gap="large")

    with chart_col1:
        fig_allocation = create_allocation_chart(df)
        st.plotly_chart(fig_allocation, use_container_width=True)

    with chart_col2:
        fig_pnl = create_pnl_chart(df)
        st.plotly_chart(fig_pnl, use_container_width=True)

    st.divider()

    st.markdown("### 📈 Portfolio Performance")

    price_history = get_portfolio_history(df)
    portfolio_history = calculate_portfolio_history(df, price_history)

    if portfolio_history.empty or "Total" not in portfolio_history.columns or len(portfolio_history) < 2:
        st.info("Portfolio performance needs at least 2 valid market data points.")
    else:
        daily_pnl, daily_pnl_percentage = calculate_daily_pnl(portfolio_history)

        start_date = portfolio_history.index.min()
        benchmark_history = get_benchmark_history(start_date)
        comparison_df = compare_with_benchmark(portfolio_history, benchmark_history, df)

        if comparison_df.empty:
            st.info("Benchmark comparison is not available for this asset/time period.")
            fig_performance = create_portfolio_performance_chart(portfolio_history)
            st.plotly_chart(fig_performance, use_container_width=True)
        else:
            portfolio_return = comparison_df["Portfolio Indexed"].iloc[-1] - 100
            sp500_return = comparison_df["S&P 500 Indexed"].iloc[-1] - 100
            performance_vs_sp500 = portfolio_return - sp500_return

            metric_col1, metric_col2 = st.columns([1, 1], gap="large")

            with metric_col1:
                st.metric(
                    "Daily PNL",
                    f"${daily_pnl:,.2f}",
                    f"{daily_pnl_percentage:.2f}%"
                )

            with metric_col2:
                st.metric(
                    "Outperformance vs S&P 500",
                    f"{performance_vs_sp500:.2f}%",
                    f"Portfolio {portfolio_return:.2f}% vs S&P 500 {sp500_return:.2f}%"
                )

            compare_sp500 = st.toggle("Compare with S&P 500")

            fig_performance = create_portfolio_performance_chart(
                portfolio_history,
                comparison_df if compare_sp500 else None
            )

            st.plotly_chart(fig_performance, use_container_width=True)

    st.divider()

    st.markdown("### 📋 Holdings")
    st.caption("Detailed view of your current positions, prices and performance.")

    df_display = prepare_display_table(df)

    df_display["PNL"] = df["PNL"].apply(
        lambda x: (
            f"🟢 ${x:,.2f}" if x > 0
            else f"🔴 ${x:,.2f}" if x < 0
            else f"⚪ ${x:,.2f}"
        )
    )

    df_display["PNL %"] = df["PNL_Percentage"].apply(
        lambda x: (
            f"🟢 {x:.2f}%" if x > 0
            else f"🔴 {x:.2f}%" if x < 0
            else f"⚪ {x:.2f}%"
        )
    )

    df_display.insert(0, "Remove", False)

    edited_df = st.data_editor(
        df_display,
        key="portfolio_editor",
        use_container_width=True,
        hide_index=True,
        column_config={
            "Remove": st.column_config.CheckboxColumn(
                "Remove",
                help="Select assets to remove",
                default=False
            ),
            "PNL": st.column_config.TextColumn("PNL"),
            "PNL %": st.column_config.TextColumn("PNL %")
        },
        disabled=[
            col for col in df_display.columns
            if col != "Remove"
        ]
    )

    if st.button("🗑️ Remove Selected"):
        selected_rows = edited_df["Remove"].astype(bool)

        if selected_rows.any():
            st.session_state.portfolio = st.session_state.portfolio[
                ~selected_rows.values
            ].reset_index(drop=True)

            st.success("Selected assets removed!")
            st.rerun()
        else:
            st.warning("No assets selected.")

else:
    st.info("No assets yet. Add your first one 👆")