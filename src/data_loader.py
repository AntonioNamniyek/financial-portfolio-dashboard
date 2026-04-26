import os

import pandas as pd
import streamlit as st

from src.portfolio import load_portfolio


EXPECTED_COLUMNS = ["ticker", "asset_name", "quantity", "buy_price", "buy_date"]


def validate_portfolio_csv(df):
    missing_columns = [col for col in EXPECTED_COLUMNS if col not in df.columns]

    if missing_columns:
        return False, missing_columns

    return True, []


def show_invalid_csv_message(missing_columns):
    st.error(
        f"""
        ❌ Invalid CSV format.

        Missing columns: {", ".join(missing_columns)}

        Expected columns:
        ticker, asset_name, quantity, buy_price, buy_date

        Example:
        ticker,asset_name,quantity,buy_price,buy_date
        AAPL,Apple,5,180,2024-01-10
        """
    )


def save_portfolio_source(source):
    st.session_state.portfolio_source = source

    with open("data/portfolio_source.txt", "w") as f:
        f.write(source)


def load_selected_portfolio():
    if "portfolio_source" not in st.session_state:
        if os.path.exists("data/portfolio_source.txt"):
            with open("data/portfolio_source.txt", "r") as f:
                st.session_state.portfolio_source = f.read().strip()
        else:
            st.session_state.portfolio_source = None

    if st.session_state.portfolio_source is None:
        uploaded_file = st.file_uploader("Upload your portfolio CSV", type=["csv"])

        if uploaded_file is not None:
            df_uploaded = pd.read_csv(uploaded_file)

            is_valid, missing_columns = validate_portfolio_csv(df_uploaded)

            if not is_valid:
                show_invalid_csv_message(missing_columns)
                st.stop()

            df_uploaded.to_csv("data/uploaded_portfolio.csv", index=False)

            save_portfolio_source("upload")
            st.rerun()

        if st.button("Use example portfolio", key="use_example_btn"):
            save_portfolio_source("example")
            st.rerun()

        st.info("Upload a CSV file or use the example portfolio to start.")
        st.stop()

    if st.button("Change portfolio", key="change_portfolio_btn"):
        st.session_state.portfolio_source = None

        if os.path.exists("data/portfolio_source.txt"):
            os.remove("data/portfolio_source.txt")

        st.rerun()

    if st.session_state.portfolio_source == "example":
        return load_portfolio("data/portfolio.csv")

    if st.session_state.portfolio_source == "upload":
        return load_portfolio("data/uploaded_portfolio.csv")

    return None