import plotly.express as px


def create_allocation_chart(df):
    fig = px.pie(
        df,
        names="ticker",
        values="current_value",
        title="Current Portfolio Allocation"
    )

    return fig


def create_pnl_chart(df):
    df = df.copy()

    df["PNL_color"] = df["PNL"].apply(lambda x: "green" if x > 0 else "red")
    df["label"] = df["PNL"].apply(
        lambda x: f"{'+' if x > 0 else ''}{x:.0f}$"
    )

    fig = px.bar(
        df,
        x="ticker",
        y="PNL",
        text="label",
        color="PNL_color",
        color_discrete_map={
            "green": "green",
            "red": "red"
        },
        title="PNL by Asset"
    )

    fig.update_traces(
        textposition="outside",
        textfont=dict(
            size=12,
            color="white"
        ),
        cliponaxis=False
    )

    fig.update_layout(
        xaxis_title=None,
        yaxis_title="PNL",
        showlegend=False,
        xaxis=dict(
            showticklabels=True,
            tickangle=0
        )
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
        textfont=dict(
            size=15,
            color="white"
        )
    )

    fig.update_layout(
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