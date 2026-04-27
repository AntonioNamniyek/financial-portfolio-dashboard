import pandas as pd


def format_currency(value):
    if pd.isna(value):
        return "N/A"

    return f"${value:,.2f}"


def format_percentage(value):
    if pd.isna(value):
        return "N/A"

    return f"{value:.2f}%"


def format_quantity(value):
    if pd.isna(value):
        return "N/A"

    return f"{int(value)}" if value >= 1 else f"{value:.4f}"


def prepare_display_table(df):
    df_display = df.copy()

    df_display["quantity"] = df_display["quantity"].map(format_quantity)
    df_display["buy_price"] = df_display["buy_price"].map(format_currency)
    df_display["current_price"] = df_display["current_price"].map(format_currency)
    df_display["invested_value"] = df_display["invested_value"].map(format_currency)
    df_display["current_value"] = df_display["current_value"].map(format_currency)
    df_display["PNL"] = df_display["PNL"].map(format_currency)
    df_display["PNL_Percentage"] = df_display["PNL_Percentage"].map(format_percentage)

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
    if value == "N/A":
        return "color: white"

    value = float(value.replace("$", "").replace(",", ""))

    if value > 0:
        return "color: green"
    elif value < 0:
        return "color: red"
    else:
        return "color: white"


def color_pnl_percentage(value):
    if value == "N/A":
        return "color: white"

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