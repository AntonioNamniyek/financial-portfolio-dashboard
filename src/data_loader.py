import os

import pandas as pd
import streamlit as st

from src.portfolio import load_portfolio


EXPECTED_COLUMNS = ["ticker", "asset_name", "quantity", "buy_price", "buy_date"]


def validate_portfolio_csv(df):
    missing_columns = [col for col in EXPECTED_COLUMNS if col not in df.columns]
    return len(missing_columns) == 0, missing_columns


def show_invalid_csv_message(missing_columns):
    st.error("❌ Invalid CSV format.")

    st.write(f"Missing columns: {', '.join(missing_columns)}")

    st.write("Expected columns:")
    st.code("ticker,asset_name,quantity,buy_price,buy_date")

    st.write("Example:")
    st.code("AAPL,Apple,5,180,2024-01-10")


def save_portfolio_source(source):
    st.session_state.portfolio_source = source

    with open("data/portfolio_source.txt", "w") as f:
        f.write(source)


def reset_portfolio_source():
    st.session_state.portfolio_source = None

    if os.path.exists("data/portfolio_source.txt"):
        os.remove("data/portfolio_source.txt")


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
        reset_portfolio_source()
        st.rerun()

    if st.session_state.portfolio_source == "example":
        return load_portfolio("data/portfolio.csv")

    if st.session_state.portfolio_source == "upload":
        if not os.path.exists("data/uploaded_portfolio.csv"):
            reset_portfolio_source()
            st.warning("Uploaded portfolio not found. Please upload a CSV again or use the example portfolio.")
            st.stop()

        df_uploaded = load_portfolio("data/uploaded_portfolio.csv")

        is_valid, missing_columns = validate_portfolio_csv(df_uploaded)

        if not is_valid:
            reset_portfolio_source()
            show_invalid_csv_message(missing_columns)
            st.stop()

        return df_uploaded

    reset_portfolio_source()
    st.stop()