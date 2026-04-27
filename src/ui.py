import streamlit as st


@st.cache_data
def load_css_file(file_path):
    with open(file_path) as f:
        return f.read()


def apply_custom_layout():
    css = load_css_file("src/styles.css")

    st.markdown(
        f"<style>{css}</style>",
        unsafe_allow_html=True
    )


def render_header(last_updated):
    st.markdown("""
    # 📊 Portfolio Market Dashboard
    Track portfolio performance, allocation, and market signals in real time.
    """)

    if st.button("🔄 Refresh Prices"):
        st.cache_data.clear()

    st.caption(f"Last updated: {last_updated}")


def render_metrics(total_invested, total_current_value, total_pnl, total_pnl_percentage):
    col1, col2, col3, col4 = st.columns(4, gap="large")

    col1.metric("Total Invested", f"${total_invested:,.2f}")
    col2.metric("Current Value", f"${total_current_value:,.2f}")

    col3.metric(
        "Total PNL",
        f"${total_pnl:,.2f}",
        delta=f"{total_pnl_percentage:.2f}%"
    )

    col4.metric(
        "Total PNL %",
        f"{total_pnl_percentage:.2f}%",
        delta=f"${total_pnl:,.2f}"
    )


def render_signal_box(trend, rsi_value, ma_diff_pct):
    if trend == "Bullish":
        final_signal = "BULLISH"
        icon = "🟢"
    elif trend == "Bearish":
        final_signal = "BEARISH"
        icon = "🔴"
    else:
        final_signal = "NEUTRAL"
        icon = "⚪"

    if rsi_value > 70:
        rsi_message = f"RSI is at {rsi_value:.2f}, asset may be overbought."
    elif rsi_value < 30:
        rsi_message = f"RSI is at {rsi_value:.2f}, asset may be oversold."
    else:
        rsi_message = f"RSI is at {rsi_value:.2f}, asset is in a neutral range."

    if ma_diff_pct > 0:
        ma_message = f"MA Diff is at {ma_diff_pct:.2f}%, so the momentum is positive."
    elif ma_diff_pct < 0:
        ma_message = f"MA Diff is at {ma_diff_pct:.2f}%, so the momentum is negative."
    else:
        ma_message = "MA Diff is at 0.00%, so the momentum is neutral."

    html = f"""
<div class="signal-box">
<div class="signal-header">
<span class="signal-icon">{icon}</span>
<span class="signal-title">{final_signal}</span>
</div>

<div class="signal-message">{rsi_message}</div>
<div class="signal-message">{ma_message}</div>
</div>
"""

    st.markdown(html, unsafe_allow_html=True)