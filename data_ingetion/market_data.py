import yfinance as yf
import datetime
import pandas as pd
import os


def portfolio_data(region: str = "IND"):
    region = "IND"
    if region == "IND":
        portfolio = "/data_ingetion/portfolios/IND.csv"
    else:
        portfolio = "/data_ingetion/portfolios/US.csv"

    pc_file = os.getcwd() + "/data_ingetion/portfolios/portfolio_change.csv"

    today = datetime.datetime.today().strftime("%Y-%m-%d")

    portfolio_change = pd.read_csv(pc_file)
    df = pd.read_csv(os.getcwd() + portfolio)

    if today not in portfolio_change.columns:
        pc = []

        for ticker in df["Ticker Symbol"]:
            pc.append(price_change(ticker, 7, True))

        portfolio_change[today] = pc

        portfolio_change.to_csv(pc_file, index=False)

    df["Price Change%"] = portfolio_change[today]
    df.drop("Date of Investment", axis=1, inplace=True)

    return f"Portfolio and change in prices in part 7 days : \n {str(df)}"


def price_change(symbol, days: int, raw: bool = False):
    stock = yf.Ticker(ticker=symbol)

    today_price = stock.history(period="1d")

    # Target date: 1 year and 7 days ago
    target_date = datetime.datetime.today() - datetime.timedelta(days=days)
    start_date = (target_date - datetime.timedelta(days=5)).strftime("%Y-%m-%d")
    end_date = (target_date + datetime.timedelta(days=1)).strftime("%Y-%m-%d")

    # Fetch range around the target date
    history = stock.history(start=start_date, end=end_date)

    # Get the latest available price before or on the target date
    past_price = history[history.index <= target_date.strftime("%Y-%m-%d")].iloc[-1]

    percentage_difference = (
        (today_price["Close"] - past_price["Close"]) / past_price["Close"]
    ).values[0] * 100

    response = (
        f"Price change for {symbol} in past {days} days is {percentage_difference:.2f}%"
    )
    if raw:
        return percentage_difference
    return response


def earning_summary(symbol):
    stock = yf.Ticker(ticker=symbol)
    metrics = [
        "EBITDA",
        "Total Expenses",
        "Basic EPS",
        "Net Income",
        "Gross Profit",
        "Total Revenue",
    ]
    currency = stock.fast_info.currency
    income_metrics = stock.income_stmt

    scaler = 1e7 if currency == "INR" else 1e6
    units = "carore" if currency == "INR" else "millions"

    selected_metric = income_metrics.loc[metrics] / scaler

    response = f"Earning metrics for {symbol} are following in {currency} currency in {units}: \n {selected_metric}"

    return response


def get_update(symbol):
    stock = yf.Ticker(ticker=symbol)
    data = stock.news
    news = ""

    for info in data[:5]:
        news += info["content"]["title"] + "\n"
        news += info["content"]["summary"] + "\n\n"

    pc = price_change(symbol, 7)

    response = f"Price change for {symbol} in past 7 days is {pc} \n\n NEWS :\n\n{news}"

    return response
