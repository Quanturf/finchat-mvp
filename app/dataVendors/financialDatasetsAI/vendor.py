import requests
import pandas as pd

from ..baseDataVendor import BaseDataVendor


class FinancialDatasetsAI(BaseDataVendor):
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.headers = {"X-API-KEY": api_key}
        self.base_url = "https://api/financialdatasets.ai"

    def get_prices(
        self,
        ticker: str,
        interval: str = "day",  # possible values are {'second', 'minute', 'day', 'week', 'month', 'year'}
        interval_multiplier: int = 1,
        start_date: str = None,
        end_date: str = None,
    ):
        """Implementation for Financial Datasets AI price data"""
        url = f"{self.base_url}/prices/"
        params = {
            "ticker": ticker,
            "interval": interval,
            "interval_multiplier": interval_multiplier,
            "start_date": start_date,
            "end_date": end_date,
        }

        response = requests.get(url, headers=self.headers, params=params)
        response.raise_for_status()

        data = response.json().get("prices", [])
        print(f"{ticker} price data: {data}")
        df = pd.DataFrame(data=data)
        return df
