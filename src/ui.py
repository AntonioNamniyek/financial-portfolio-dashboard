import streamlit as st


def apply_custom_layout():
    st.set_page_config(layout="wide")

    st.markdown("""
    <style>
    .main .block-container {
        max-width: 1000px;
        margin-left: auto;
        margin-right: auto;
        padding-left: 2rem;
        padding-right: 2rem;
    }
    </style>
    """, unsafe_allow_html=True)


def render_header(last_updated):
    st.markdown("""
    # 📊 Portfolio Market Dashboard
    Track portfolio performance, allocation, and market signals in real time.
    """)

    if st.button("🔄 Refresh Prices"):
        st.cache_data.clear()

    st.caption(f"Last updated: {last_updated}")


def render_metrics(total_invested, total_current_value, total_pnl, total_pnl_percentage):
    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Total Invested", f"${total_invested:,.2f}")
    col2.metric("Current Value", f"${total_current_value:,.2f}")
    col3.metric("Total PNL", f"${total_pnl:,.2f}")
    col4.metric("Total PNL %", f"{total_pnl_percentage:.2f}%")