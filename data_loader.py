import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta

def fetch_stock_data(ticker: str, period: str = "1y") -> pd.DataFrame:
    """
    Fetch historical stock data for the given ticker and period.
    Default period is 1 year.
    """
    data = yf.download(ticker, period=period, interval="1d")
    data.dropna(inplace=True)
    return data

if __name__ == "__main__":
    # Example usage: fetch data for Apple for the past year
    df = fetch_stock_data("AAPL")
    print(df.head())
