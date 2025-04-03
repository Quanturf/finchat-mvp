import requests
import pandas as pd
import logging
from typing import Optional

from ..baseDataVendor import BaseDataVendor

logger = logging.getLogger(__name__)


class FinancialDatasetsAI(BaseDataVendor):
    def __init__(self, api_key: str):
        if not api_key:
            raise ValueError("API key is required for FinancialDatasetsAI.")
        self.api_key = api_key
        self.headers = {"X-API-KEY": api_key}
        self.base_url = "https://api.financialdatasets.ai"

    def get_prices(
        self,
        ticker: str,
        interval: str = "day",
        interval_multiplier: int = 1,
        start_date: str = None,
        end_date: str = None,
        period: Optional[str] = None,
    ) -> pd.DataFrame:
        logger.warning(
            "FinancialDatasetsAI provider is not fully implemented (using placeholder URL)."
        )
        url = f"{self.base_url}/prices/"
        params = {
            "ticker": ticker,
            "interval": interval,
            "interval_multiplier": interval_multiplier,
            "start_date": start_date,
            "end_date": end_date,
        }
        params = {k: v for k, v in params.items() if v is not None}

        try:
            response = requests.get(
                url, headers=self.headers, params=params, timeout=10
            )
            response.raise_for_status()
            data = response.json().get("prices", [])
            logger.info(
                f"Received price data for {ticker} from FinancialDatasetsAI (mocked/placeholder)."
            )
            df = pd.DataFrame(data=data)
            if "date" in df.columns:
                df["date"] = pd.to_datetime(df["date"])
                df.set_index("date", inplace=True)
            return df
        except requests.exceptions.RequestException as e:
            logger.error(
                f"API Error fetching prices from FinancialDatasetsAI for {ticker}: {e}"
            )
            return pd.DataFrame()
        except Exception as e:
            logger.error(
                f"Error processing price data from FinancialDatasetsAI for {ticker}: {e}"
            )
            return pd.DataFrame()

    def get_financial_statements(
        self, ticker: str, statement_type: str, period: str
    ) -> pd.DataFrame:
        logger.warning("FinancialDatasetsAI get_financial_statements not implemented.")
        return pd.DataFrame()

    def get_company_info(self, ticker: str):
        logger.warning("FinancialDatasetsAI get_company_info not implemented.")
        return None

    def get_institutional_holders(self, ticker: str) -> pd.DataFrame:
        logger.warning("FinancialDatasetsAI get_institutional_holders not implemented.")
        return pd.DataFrame()

    def get_sec_filings(self, ticker: str):
        logger.warning("FinancialDatasetsAI get_sec_filings not implemented.")
        return []

    def get_news(self, ticker: str):
        logger.warning("FinancialDatasetsAI get_news not implemented.")
        return []
