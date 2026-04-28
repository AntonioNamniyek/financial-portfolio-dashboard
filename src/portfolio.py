import pandas as pd
import yfinance as yf


def load_portfolio(path):
    return pd.read_csv(path)


def normalize_ticker(ticker):
    ticker = str(ticker).upper().strip()

    if ticker.startswith("^"):
        return ticker

    if "-" in ticker:
        return ticker

    if ticker.endswith("USD") and len(ticker) > 3:
        return ticker[:-3] + "-USD"

    return ticker

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
        yf_ticker = normalize_ticker(ticker)

        try:
            stock = yf.Ticker(yf_ticker)
            history = stock.history(start=start_date)

            if history.empty or "Close" not in history.columns:
                continue

            close_prices = history["Close"].dropna()

            if close_prices.empty:
                continue

            close_prices.index = pd.to_datetime(close_prices.index).tz_localize(None).date
            close_prices = close_prices.groupby(close_prices.index).last()

            all_data[ticker] = close_prices

        except Exception:
            continue

    price_history = pd.DataFrame(all_data)

    if price_history.empty:
        return price_history

    price_history.index = pd.to_datetime(price_history.index)

    return price_history.sort_index()


def calculate_portfolio_history(df, price_history):
    portfolio_history = pd.DataFrame(index=price_history.index)

    for _, row in df.iterrows():
        ticker = row["ticker"]
        quantity = row["quantity"]
        buy_date = pd.to_datetime(row["buy_date"])

        if ticker not in price_history.columns:
            continue

        asset_value = price_history[ticker] * quantity
        asset_value = asset_value.where(price_history.index >= buy_date, 0)

        portfolio_history[ticker] = asset_value

    if portfolio_history.empty:
        return portfolio_history

    portfolio_history = portfolio_history.ffill().fillna(0)
    portfolio_history["Total"] = portfolio_history.sum(axis=1)

    return portfolio_history


def calculate_daily_pnl(portfolio_history):
    if portfolio_history.empty or "Total" not in portfolio_history.columns or len(portfolio_history) < 2:
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
    try:
        stock = yf.Ticker(benchmark)
        history = stock.history(start=start_date)

        if history.empty or "Close" not in history.columns:
            return pd.Series(dtype="float64")

        return history["Close"].dropna()

    except Exception:
        return pd.Series(dtype="float64")


def compare_with_benchmark(portfolio_history, benchmark_history):
    if portfolio_history.empty or "Total" not in portfolio_history.columns:
        return pd.DataFrame()

    benchmark_history = benchmark_history.copy()
    benchmark_history.index = pd.to_datetime(benchmark_history.index).tz_localize(None)

    portfolio = portfolio_history["Total"].copy()
    portfolio.index = pd.to_datetime(portfolio.index)

    # 🔥 INTERSEÇÃO REAL DE DATAS
    common_index = portfolio.index.intersection(benchmark_history.index)

    if len(common_index) < 2:
        return pd.DataFrame()

    portfolio = portfolio.loc[common_index]
    benchmark = benchmark_history.loc[common_index]

    comparison = pd.DataFrame({
        "Portfolio": portfolio,
        "Benchmark": benchmark
    })

    # 🔥 NORMALIZAÇÃO CORRETA
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