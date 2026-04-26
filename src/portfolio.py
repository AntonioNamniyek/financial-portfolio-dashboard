import pandas as pd

def load_portfolio(path):
    return pd.read_csv(path)

def calculate_portfolio_values(df):
    df["invested_value"] = df["quantity"] * df["buy_price"]
    df["current_value"] = df["quantity"] * df["current_price"]
    df["PNL"] = df["current_value"] - df["invested_value"]
    df["PNL_Percentage"] = df["PNL"] * 100 / df["invested_value"]
    return df

def calculate_totals(df):
    total_invested = df["invested_value"].sum()
    total_current_value = df["current_value"].sum()
    total_pnl = df["PNL"].sum()
    total_pnl_percentage = total_pnl * 100 / total_invested

    return total_invested, total_current_value, total_pnl, total_pnl_percentage