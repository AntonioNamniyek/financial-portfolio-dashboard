import pandas as pd
import yfinance as yf


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

    if total_invested > 0:
        total_pnl_percentage = total_pnl * 100 / total_invested
    else:
        total_pnl_percentage = 0

    return total_invested, total_current_value, total_pnl, total_pnl_percentage


def get_portfolio_history(df):
    all_data = {}

    start_date = pd.to_datetime(df["buy_date"]).min()

    for ticker in df["ticker"].unique():
        stock = yf.Ticker(ticker)
        history = stock.history(start=start_date)["Close"]
        all_data[ticker] = history

    return pd.DataFrame(all_data)


def calculate_portfolio_history(df, price_history):
    portfolio_history = pd.DataFrame(index=price_history.index)

    for _, row in df.iterrows():
        ticker = row["ticker"]
        quantity = row["quantity"]
        buy_date = pd.to_datetime(row["buy_date"]).date()

        asset_value = price_history[ticker] * quantity

        asset_value.index = asset_value.index.date
        asset_value = asset_value.where(asset_value.index >= buy_date, 0)

        portfolio_history[ticker] = asset_value.values

    portfolio_history["Total"] = portfolio_history.sum(axis=1)

    return portfolio_history


def calculate_daily_pnl(portfolio_history):
    if portfolio_history.empty or len(portfolio_history) < 2:
        return 0, 0

    current_value = portfolio_history["Total"].iloc[-1]
    previous_value = portfolio_history["Total"].iloc[-2]

    daily_pnl = current_value - previous_value

    if previous_value > 0:
        daily_pnl_percentage = daily_pnl * 100 / previous_value
    else:
        daily_pnl_percentage = 0

    return daily_pnl, daily_pnl_percentage


def get_benchmark_history(start_date, benchmark="^GSPC"):
    stock = yf.Ticker(benchmark)
    history = stock.history(start=start_date)["Close"]

    return history


def compare_with_benchmark(portfolio_history, benchmark_history):
    comparison = pd.DataFrame(index=portfolio_history.index)

    comparison["Portfolio"] = portfolio_history["Total"]
    comparison["Benchmark"] = benchmark_history.reindex(portfolio_history.index).ffill()

    comparison = comparison.dropna()

    comparison["Portfolio Indexed"] = (
        comparison["Portfolio"] / comparison["Portfolio"].iloc[0] * 100
    )

    comparison["S&P 500 Indexed"] = (
        comparison["Benchmark"] / comparison["Benchmark"].iloc[0] * 100
    )

    return comparison


def calculate_vs_benchmark(comparison_df):
    if comparison_df.empty:
        return 0, 0, 0

    portfolio_return = comparison_df["Portfolio Indexed"].iloc[-1] - 100
    benchmark_return = comparison_df["S&P 500 Indexed"].iloc[-1] - 100
    difference = portfolio_return - benchmark_return

    return portfolio_return, benchmark_return, difference