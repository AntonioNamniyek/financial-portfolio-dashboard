import streamlit as st

from src.ui import apply_custom_layout


st.set_page_config(
    page_title="Portfolio Dashboard",
    page_icon="📊",
    layout="wide"
)

apply_custom_layout()

st.title("📊 Portfolio Dashboard")
st.caption("Track your holdings, performance, allocation and market signals.")

st.markdown("""
### Welcome

Use the sidebar to navigate:

- **Portfolio** — add assets, track value, PNL and allocation
- **Analysis** — search assets, view TradingView charts and indicators
""")