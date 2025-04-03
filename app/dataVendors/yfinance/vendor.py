import yfinance as yf
import pandas as pd
from typing import Optional
from ..baseDataVendor import BaseDataVendor


class YahooFinance(BaseDataVendor):
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key

    def get_prices(
        self,
        ticker: str,
        interval: str = "1d",
        interval_multiplier: int = 1,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
    ) -> pd.DataFrame:
        """Get ticker price data using yfinance."""
        try:
            yf_interval_map = {
                "second": "1s",
                "minute": "1m",
                "day": "1d",
                "week": "1wk",
                "month": "1mo",
                "year": "1y",
            }

            yf_interval = yf_interval_map.get(interval, "1d")

            company = yf.Ticker(ticker)
            if start_date and end_date:
                history = company.history(
                    start=start_date, end=end_date, interval=yf_interval
                )
            else:
                history = company.history(period="1d", interval=yf_interval)
            return history
        except Exception as e:
            print(f"Error fetching price data from yfinance: {e}")
            return pd.DataFrame()  # Return an empty DataFrame on error

    def get_financial_statements(
        self,
        ticker: str,
        statement_type: str,  # income_statement, balance_sheet, cash_flow_statement
        period: str = "annual",  # or "quarterly
    ) -> pd.DataFrame:
        """Get financial statements using yfinance"""
        try:
            company = yf.Ticker(ticker)
            if statement_type == "income_statement":
                if period == "annual":
                    return company.income_stmt
                elif period == "quarterly":
                    return company.quarterly_income_stmt
            elif statement_type == "balance_sheet":
                if period == "annual":
                    return company.balance_sheet
                elif period == "quarterly":
                    return company.quarterly_balance_sheet
            elif statement_type == "cash_flow_statement":
                if period == "annual":
                    return company.cashflow
                elif period == "quarterly":
                    return company.quarterly_cashflow
            else:
                raise ValueError(
                    "Invalid statement_type. Choose 'income_statement', 'balance_sheet', or 'cash_flow_statement'."
                )

        except Exception as e:
            print(f"Error fetching financial statements from yfinance: {e}")
            return pd.DataFrame()

    def get_company_info(self, ticker: str):
        """Get company information using yfinance"""
        try:
            company = yf.Ticker(ticker)
            return pd.Series(company.info)
        except Exception as e:
            print(f"Error fetching company info from yfinance: {e}")
            return pd.Series()

    def get_institutional_holders(self, ticker: str) -> pd.DataFrame:
        try:
            company = yf.Ticker(ticker)
            return company.institutional_holders
        except Exception as e:
            print(f"Error fetching company info from yfinance: {e}")
            return pd.DataFrame()

    def get_sec_filings(self, ticker: str):
        try:
            company = yf.Ticker(ticker)
            return company.get_sec_filings()
        except Exception as e:
            print(f"Error fetching company info from yfinance: {e}")
            return pd.DataFrame()

    def get_news(self, ticker: str):
        try:
            company = yf.Ticker(ticker)
            return pd.Series(company.news)
        except Exception as e:
            print(f"Error fetching company info from yfinance: {e}")
            return pd.Series()

    def get_earnings_history(self, ticker: str):
        try:
            company = yf.Ticker(ticker)
            return company.earnings_history
        except Exception as e:
            print(f"Error fetching company info from yfinance: {e}")
            return pd.DataFrame()
