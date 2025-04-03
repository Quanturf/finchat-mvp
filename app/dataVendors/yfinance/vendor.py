import yfinance as yf
import pandas as pd
from typing import Optional, List, Dict
import logging
from ..baseDataVendor import BaseDataVendor

logger = logging.getLogger(__name__)


class YahooFinance(BaseDataVendor):
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key

    def get_prices(
        self,
        ticker: str,
        interval: str = "1d",
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        period: Optional[str] = None,
    ) -> pd.DataFrame:
        yf_interval_map = {
            "second": "1m",  # yfinance min interval is 1m for recent data
            "minute": "1m",
            "day": "1d",
            "week": "1wk",
            "month": "1mo",
            "year": "1y",
        }
        yf_interval = yf_interval_map.get(interval, "1d")

        try:
            company = yf.Ticker(ticker)
            history = company.history(
                start=start_date, end=end_date, interval=yf_interval, period=period
            )
            if history.empty:
                logger.warning(
                    f"No price data returned from yfinance for {ticker} with parameters: start={start_date}, end={end_date}, interval={yf_interval}, period={period}"
                )
            else:
                logger.info(
                    f"Successfully fetched {len(history)} price data points for {ticker} from yfinance."
                )
            return history
        except Exception as e:
            logger.error(f"Error fetching price data from yfinance for {ticker}: {e}")
            return pd.DataFrame()

    def get_financial_statements(
        self,
        ticker: str,
        statement_type: str,
        period: str = "annual",
    ) -> pd.DataFrame:
        try:
            company = yf.Ticker(ticker)
            statement = None
            if statement_type == "income_statement":
                statement = (
                    company.income_stmt
                    if period == "annual"
                    else company.quarterly_income_stmt
                )
            elif statement_type == "balance_sheet":
                statement = (
                    company.balance_sheet
                    if period == "annual"
                    else company.quarterly_balance_sheet
                )
            elif statement_type == "cash_flow_statement":
                statement = (
                    company.cashflow
                    if period == "annual"
                    else company.quarterly_cashflow
                )
            else:
                raise ValueError(f"Invalid statement_type '{statement_type}'.")

            if statement.empty:
                logger.warning(
                    f"No {period} {statement_type} data returned from yfinance for {ticker}."
                )
            else:
                logger.info(
                    f"Successfully fetched {period} {statement_type} for {ticker} from yfinance."
                )
            return statement

        except Exception as e:
            logger.error(
                f"Error fetching {period} {statement_type} from yfinance for {ticker}: {e}"
            )
            return pd.DataFrame()

    def get_company_info(self, ticker: str) -> Optional[pd.Series]:
        try:
            company = yf.Ticker(ticker)
            info = company.info
            if not info or info.get("quoteType") == "MUTUALFUND":  # Example check
                logger.warning(
                    f"No substantial company info returned from yfinance for {ticker} or unsupported type."
                )
                return None
            logger.info(
                f"Successfully fetched company info for {ticker} from yfinance."
            )
            # Convert dict to Series before returning
            return pd.Series(info)
        except Exception as e:
            # yfinance often raises generic exceptions or returns empty dicts for invalid tickers
            logger.warning(
                f"Could not fetch company info from yfinance for {ticker}: {e}"
            )
            return None

    def get_institutional_holders(self, ticker: str) -> pd.DataFrame:
        try:
            company = yf.Ticker(ticker)
            holders = company.institutional_holders
            if holders.empty:
                logger.warning(
                    f"No institutional holders data returned from yfinance for {ticker}."
                )
            else:
                logger.info(
                    f"Successfully fetched institutional holders for {ticker} from yfinance."
                )
            return holders
        except Exception as e:
            logger.error(
                f"Error fetching institutional holders from yfinance for {ticker}: {e}"
            )
            return pd.DataFrame()

    def get_sec_filings(self, ticker: str) -> List[Dict]:
        try:
            company = yf.Ticker(ticker)
            filings_result = company.get_sec_filings()

            filings_list = []
            if isinstance(filings_result, pd.DataFrame) and not filings_result.empty:
                filings_result = filings_result.replace({pd.NA: None, pd.NaT: None})
                filings_list = filings_result.to_dict(orient="records")
            elif isinstance(filings_result, list):
                filings_list = filings_result
            elif filings_result is None or (
                hasattr(filings_result, "empty") and filings_result.empty
            ):
                logger.warning(f"No SEC filings returned from yfinance for {ticker}.")
                return []
            else:
                logger.warning(
                    f"Unexpected type returned by yfinance get_sec_filings for {ticker}: {type(filings_result)}"
                )
                return []

            logger.info(
                f"Successfully fetched {len(filings_list)} SEC filings for {ticker} from yfinance."
            )
            return filings_list
        except Exception as e:
            logger.error(f"Error fetching SEC filings from yfinance for {ticker}: {e}")
            return []

    def get_news(self, ticker: str) -> List[Dict]:
        try:
            company = yf.Ticker(ticker)
            news = company.news
            if not news:
                logger.warning(f"No news returned from yfinance for {ticker}.")
                return []
            logger.info(f"Successfully fetched news for {ticker} from yfinance.")
            return news  # Assumes yfinance returns a list of dicts
        except Exception as e:
            logger.error(f"Error fetching news from yfinance for {ticker}: {e}")
            return []

    def get_earnings_history(self, ticker: str) -> pd.DataFrame:
        try:
            company = yf.Ticker(ticker)
            earnings = company.earnings_history
            if earnings.empty:
                logger.warning(
                    f"No earnings history returned from yfinance for {ticker}."
                )
            else:
                logger.info(
                    f"Successfully fetched earnings history for {ticker} from yfinance."
                )
            return earnings
        except Exception as e:
            logger.error(
                f"Error fetching earnings history from yfinance for {ticker}: {e}"
            )
            return pd.DataFrame()
