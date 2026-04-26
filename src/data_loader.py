import os
import streamlit as st

from src.portfolio import load_portfolio


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
            with open("data/uploaded_portfolio.csv", "wb") as f:
                f.write(uploaded_file.getbuffer())

            st.session_state.portfolio_source = "upload"

            with open("data/portfolio_source.txt", "w") as f:
                f.write("upload")

            st.rerun()

        if st.button("Use example portfolio", key="use_example_btn"):
            st.session_state.portfolio_source = "example"

            with open("data/portfolio_source.txt", "w") as f:
                f.write("example")

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