from typing import Optional

from .dataVendorFactory import DataVendorFactory


def get_ticker_price(
    ticker: str,
    data_vendor: str = "yfinance",
    api_key: Optional[str] = None,
):
    """
    Fetches the latest price for a given ticker using the specified data vendor.

    Args:
        ticker: The stock ticker symbol.
        data_vendor: The data vendor to use (e.g., "yfinance").
        api_key: api_key for data vendor

    Returns:
        A JSON string containing the ticker and its price, or an error message.
    """
    try:
        vendor = DataVendorFactory.get_vendor()
        print("vendor: ", vendor)
        price = vendor.get_prices(ticker)
        if price is None:
            return {
                "error": f"Unable to retrieve price for {ticker} using {data_vendor}."
            }
        return {"price": price}
    except Exception as e:
        return f"Error: {e}"
