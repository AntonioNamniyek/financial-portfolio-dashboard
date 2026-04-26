def prepare_display_table(df):
    df_display = df.copy()

    df_display["quantity"] = df_display["quantity"].map(
        lambda x: f"{int(x)}" if x >= 1 else f"{x:.4f}"
    )

    df_display["buy_price"] = df_display["buy_price"].map(lambda x: f"${x:,.2f}")
    df_display["current_price"] = df_display["current_price"].map(lambda x: f"${x:,.2f}")
    df_display["invested_value"] = df_display["invested_value"].map(lambda x: f"${x:,.2f}")
    df_display["current_value"] = df_display["current_value"].map(lambda x: f"${x:,.2f}")
    df_display["PNL"] = df_display["PNL"].map(lambda x: f"${x:,.2f}")
    df_display["PNL_Percentage"] = df_display["PNL_Percentage"].map(lambda x: f"{x:.2f}%")

    df_display = df_display.rename(columns={
        "ticker": "Ticker",
        "asset_name": "Asset",
        "quantity": "Quantity",
        "buy_price": "Buy Price",
        "buy_date": "Buy Date",
        "current_price": "Current Price",
        "invested_value": "Invested Value",
        "current_value": "Current Value",
        "PNL": "PNL",
        "PNL_Percentage": "PNL %"
    })

    return df_display


def color_pnl(value):
    value = float(value.replace("$", "").replace(",", ""))

    if value > 0:
        return "color: green"
    elif value < 0:
        return "color: red"
    else:
        return "color: white"


def color_pnl_percentage(value):
    value = float(value.replace("%", ""))

    if value > 0:
        return "color: green"
    elif value < 0:
        return "color: red"
    else:
        return "color: white"


def style_display_table(df_display):
    return df_display.style \
        .map(color_pnl, subset=["PNL"]) \
        .map(color_pnl_percentage, subset=["PNL %"])