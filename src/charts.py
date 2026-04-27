import plotly.express as px


def create_allocation_chart(df):
    fig = px.pie(
        df,
        names="ticker",
        values="current_value",
        hole=0.55,
        title="Current Portfolio Allocation"
    )

    fig.update_traces(
        textinfo="percent+label",
        textfont_size=13,
        marker=dict(line=dict(color="#0b0f19", width=2))
    )

    fig.update_layout(
        template="plotly_dark",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="white"),
        title=dict(font=dict(size=18), x=0.02),
        legend=dict(orientation="h", y=-0.15, x=0),
        margin=dict(l=20, r=20, t=60, b=40),
        height=420
    )

    return fig


def create_pnl_chart(df):
    df = df.copy()

    df["PNL_color"] = df["PNL"].apply(lambda x: "Profit" if x >= 0 else "Loss")
    df["label"] = df["PNL"].apply(lambda x: f"{'+' if x >= 0 else ''}${x:,.0f}")

    fig = px.bar(
        df,
        x="ticker",
        y="PNL",
        text="label",
        color="PNL_color",
        color_discrete_map={
            "Profit": "#22c55e",
            "Loss": "#ef4444"
        },
        title="PNL by Asset"
    )

    fig.update_traces(
        textposition="outside",
        textfont=dict(size=13, color="white"),
        marker_line_width=0,
        cliponaxis=False
    )

    fig.update_layout(
        template="plotly_dark",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="white"),
        title=dict(font=dict(size=18), x=0.02),
        xaxis=dict(title=None, showgrid=False),
        yaxis=dict(
            title="PNL",
            gridcolor="rgba(255,255,255,0.08)",
            zerolinecolor="rgba(255,255,255,0.25)"
        ),
        showlegend=False,
        margin=dict(l=20, r=20, t=60, b=40),
        height=420
    )

    fig.add_hline(
        y=0,
        line_dash="dash",
        line_color="rgba(255,255,255,0.35)"
    )

    return fig


def create_moving_average_chart(signals_df):
    fig = px.bar(
        signals_df,
        x="Ticker",
        y=["MA20", "MA50"],
        barmode="group",
        title="Moving Averages by Asset"
    )

    fig.update_layout(
        template="plotly_dark",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        xaxis_title=None,
        yaxis_title="Price",
        legend_title=None
    )

    return fig


def create_ma_diff_chart(signals_df):
    signals_df = signals_df.copy()

    signals_df["label"] = signals_df.apply(
        lambda row: f"{row['Ticker']}<br><span style='font-size:12px'>{row['MA_diff_pct']:.2f}%</span>",
        axis=1
    )

    max_abs = signals_df["MA_diff_pct"].abs().max()

    fig = px.bar(
        signals_df,
        x="Ticker",
        y="MA_diff_pct",
        text="label",
        color="MA_diff_pct",
        color_continuous_scale=[
            [0.00, "darkred"],
            [0.50, "lightcoral"],
            [0.50, "lightgreen"],
            [1.00, "darkgreen"]
        ],
        range_color=[-max_abs, max_abs],
        title="MA20 vs MA50 Difference (%)"
    )

    fig.update_traces(
        textposition="inside",
        insidetextanchor="middle",
        textfont=dict(size=15, color="white")
    )

    fig.update_layout(
        template="plotly_dark",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        xaxis_title=None,
        yaxis_title="% Difference",
        coloraxis_colorbar=dict(title="MA % Diff"),
        xaxis=dict(showticklabels=False)
    )

    fig.add_hline(
        y=0,
        line_dash="dash",
        line_color="gray",
        opacity=0.6
    )

    return fig


def create_portfolio_performance_chart(history_df, comparison_df=None):
    if comparison_df is not None:
        chart_df = comparison_df[[
            "Portfolio Indexed",
            "S&P 500 Indexed"
        ]]

        fig = px.line(
            chart_df,
            x=chart_df.index,
            y=["Portfolio Indexed", "S&P 500 Indexed"],
            title="Portfolio Performance vs S&P 500"
        )

        yaxis_title = "Indexed Performance"

    else:
        fig = px.line(
            history_df,
            x=history_df.index,
            y="Total",
            title="Portfolio Value Over Time"
        )

        yaxis_title = "Portfolio Value"

    fig.update_layout(
        template="plotly_dark",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="white"),
        title=dict(font=dict(size=18), x=0.02),
        xaxis=dict(title=None, showgrid=False),
        yaxis=dict(
            title=yaxis_title,
            gridcolor="rgba(255,255,255,0.08)"
        ),
       legend=dict(
        orientation="h",
        y=-0.2,
        x=0,
        title_text=""
),
        margin=dict(l=20, r=20, t=60, b=60),
        height=420
    )

    fig.update_traces(
        line=dict(width=2.5)
    )

    return fig