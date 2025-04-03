from typing import Optional, Dict, Any
import pandas as pd
from .dataVendorFactory import DataVendorFactory


def get_ticker_price(
    ticker: str,
    data_vendor: str = "yfinance",
    api_key: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Fetches the latest price for a given ticker using the specified data vendor.

    Args:
        ticker: The stock ticker symbol.
        data_vendor: The data vendor to use (e.g., "yfinance").
        api_key: API key for the data vendor (if required).

    Returns:
        A dictionary containing the ticker and its price, or an error message.
    """
    try:
        vendor = DataVendorFactory.get_vendor(vendor_name=data_vendor, api_key=api_key)
        price_df = vendor.get_prices(ticker)
        if price_df.empty:
            return {
                "error": f"Unable to retrieve price for {ticker} using {data_vendor}."
            }
        if isinstance(price_df, pd.DataFrame):
            latest_close = price_df["Close"].iloc[-1]
        else:
            latest_close = price_df.iloc[-1]

        return {"ticker": ticker, "price": latest_close}
    except Exception as e:
        return {"error": str(e)}


def get_ticker_history(
    ticker: str,
    data_vendor: str = "yfinance",
    api_key: Optional[str] = None,
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    interval: str = "day",
) -> Dict[str, Any]:
    """Fetches historical price data for a given ticker."""
    try:
        vendor = DataVendorFactory.get_vendor(vendor_name=data_vendor, api_key=api_key)
        history_df = vendor.get_prices(
            ticker=ticker, start_date=start_date, end_date=end_date, interval=interval
        )
        if history_df.empty:
            return {"error": f"No historical data found for {ticker}."}
        history_dict = history_df.to_dict(orient="records")
        return {
            "ticker": ticker,
            "historical_data": history_dict,
            "start_date": start_date,
            "end_date": end_date,
            "interval": interval,
        }
    except Exception as e:
        return {"error": str(e)}


def get_company_info(
    ticker: str, data_vendor: str = "yfinance", api_key: Optional[str] = None
) -> Dict[str, Any]:
    """Fetches company information for a given ticker"""
    try:
        vendor = DataVendorFactory.get_vendor(vendor_name=data_vendor, api_key=api_key)
        company_info = vendor.get_company_info(ticker=ticker)
        if company_info.empty:
            return {"error": f"No company information found for {ticker}."}
        return {"ticker": ticker, "company_info": company_info.to_dict()}
    except Exception as e:
        return {"error": str(e)}


def get_institutional_investors(
    ticker: str, data_vendor: str = "yfinance", api_key: Optional[str] = None
) -> Dict[str, Any]:
    """Fetches institutional investors for a given ticker"""
    try:
        vendor = DataVendorFactory.get_vendor(vendor_name=data_vendor, api_key=api_key)
        institutional_investors = vendor.get_institutional_holders(ticker=ticker)
        if institutional_investors.empty:
            return {"error": f"No institutional investors data found for {ticker}."}
        return {
            "ticker": ticker,
            "institutional_investors": institutional_investors.to_dict(
                orient="records"
            ),
        }
    except Exception as e:
        return {"error": str(e)}


def get_sec_filings(
    ticker: str,
    data_vendor: str = "yfinance",
    api_key: Optional[str] = None,
    filing_type: Optional[str] = None,
) -> Dict[str, Any]:
    """Fetches SEC filings for a given ticker"""
    try:
        vendor = DataVendorFactory.get_vendor(vendor_name=data_vendor, api_key=api_key)
        sec_filings = vendor.get_sec_filings(ticker=ticker)
        if sec_filings.empty:
            return {"error": f"No SEC filings data found for {ticker}."}
        sec_filings = (
            sec_filings[sec_filings["form"] == filing_type]
            if filing_type
            else sec_filings
        )
        return {"ticker": ticker, "sec_filings": sec_filings.to_dict(orient="records")}

    except Exception as e:
        return {"error": str(e)}


def get_financial_statements(
    ticker: str,
    data_vendor: str = "yfinance",
    api_key: Optional[str] = None,
    statement_type: str = "income_statement",
    period: str = "annual",
) -> Dict[str, Any]:
    """Fetches financial statements for a given ticker"""
    try:
        vendor = DataVendorFactory.get_vendor(vendor_name=data_vendor, api_key=api_key)
        financial_statements = vendor.get_financial_statements(
            ticker=ticker, statement_type=statement_type, period=period
        )
        if financial_statements.empty:
            return {"error": f"No financial statements data found for {ticker}."}
        return {
            "ticker": ticker,
            "financial_statements": financial_statements.to_dict(),
            "statement_type": statement_type,
            "period": period,
        }
    except Exception as e:
        return {"error": str(e)}


def get_financial_news(
    ticker: str, data_vendor: str = "yfinance", api_key: Optional[str] = None
) -> Dict[str, Any]:
    """Fetches financial news for a given ticker"""
    try:
        vendor = DataVendorFactory.get_vendor(vendor_name=data_vendor, api_key=api_key)
        news = vendor.get_news(ticker=ticker)
        if news.empty:
            return {"error": f"No news found for {ticker}."}
        return {"ticker": ticker, "news": news[:3].to_dict()}
    except Exception as e:
        return {"error": str(e)}
