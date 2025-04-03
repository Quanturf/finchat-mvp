from typing import Optional, Dict, Any, List
import pandas as pd
import numpy as np
import json
import logging
from .dataVendorFactory import DataVendorFactory
from datetime import datetime, timedelta
from .functionToolSchema import AVAILABLE_TOOLS

logger = logging.getLogger(__name__)


def safe_float(value):
    if pd.isna(value):
        return None
    try:
        # Handle potential numpy types explicitly before float conversion
        if isinstance(value, (np.int64, np.int32, np.int16, np.int8)):
            value = int(value)
        elif isinstance(value, (np.float64, np.float32, np.float16)):
            value = float(value)
        # Now try converting to float
        return float(value)
    except (TypeError, ValueError):
        try:
            # Fallback to string if float conversion fails
            return str(value)
        except Exception:
            return None  # Final fallback if str conversion also fails


def get_ticker_price(
    ticker: str,
    data_vendor: str = "yfinance",
    api_key: Optional[str] = None,
) -> Dict[str, Any]:
    try:
        vendor = DataVendorFactory.get_vendor(vendor_name=data_vendor, api_key=api_key)
        price_df = vendor.get_prices(
            ticker, interval="day", period="5d"
        )  # Fetch last 5 days for change calc
        if price_df.empty or len(price_df) < 1:
            logger.warning(
                f"Unable to retrieve sufficient price data for {ticker} using {data_vendor}."
            )
            return {
                "error": f"Unable to retrieve price for {ticker} using {data_vendor}."
            }

        latest_close = safe_float(price_df["Close"].iloc[-1])
        previous_close = (
            safe_float(price_df["Close"].iloc[-2]) if len(price_df) > 1 else None
        )

        change = None
        change_percent = None
        if latest_close is not None and previous_close is not None:
            change = safe_float(latest_close - previous_close)
            if previous_close != 0:
                change_percent = (
                    safe_float((change / previous_close) * 100)
                    if change is not None
                    else None
                )

        result = {
            "ticker": ticker,
            "price": latest_close,
            "change": change,
            "change_percent": change_percent,
        }
        logger.info(f"Price fetched for {ticker}: {result}")
        return result
    except Exception as e:
        logger.exception(f"Error fetching price for {ticker}: {e}")
        return {"error": f"Error fetching price for {ticker}: {str(e)}"}


def get_ticker_history(
    ticker: str,
    data_vendor: str = "yfinance",
    api_key: Optional[str] = None,
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    interval: str = "day",
) -> Dict[str, Any]:
    try:
        vendor = DataVendorFactory.get_vendor(vendor_name=data_vendor, api_key=api_key)

        # Default date range if none provided (e.g., last 1 month)
        if not start_date or not end_date:
            today = datetime.today()
            end_date_dt = today
            start_date_dt = today - timedelta(days=30)
            end_date = end_date_dt.strftime("%Y-%m-%d")
            start_date = start_date_dt.strftime("%Y-%m-%d")
            logger.info(
                f"Defaulting date range for {ticker} history to: {start_date} - {end_date}"
            )

        history_df = vendor.get_prices(
            ticker=ticker, start_date=start_date, end_date=end_date, interval=interval
        )
        if history_df.empty:
            logger.warning(
                f"No historical data found for {ticker} from {data_vendor} for the period."
            )
            return {
                "error": f"No historical data found for {ticker} covering the specified period {start_date} to {end_date}."
            }

        summary = {}
        first_valid_index = history_df["Close"].first_valid_index()
        last_valid_index = history_df["Close"].last_valid_index()

        if first_valid_index is not None and last_valid_index is not None:
            start_price = safe_float(history_df.loc[first_valid_index, "Close"])
            end_price = safe_float(history_df.loc[last_valid_index, "Close"])

            price_change = None
            price_change_percent = None
            if start_price is not None and end_price is not None:
                price_change = safe_float(end_price - start_price)
                if start_price != 0:
                    price_change_percent = (
                        safe_float((price_change / start_price) * 100)
                        if price_change is not None
                        else None
                    )

            summary = {
                "period_start_date": str(history_df.index.min().date()),
                "period_end_date": str(history_df.index.max().date()),
                "start_price": start_price,
                "end_price": end_price,
                "period_high": safe_float(history_df["High"].max()),
                "period_low": safe_float(history_df["Low"].min()),
                "average_closing_price": safe_float(history_df["Close"].mean()),
                "average_volume": safe_float(history_df["Volume"].mean()),
                "total_volume": (
                    int(history_df["Volume"].sum())
                    if pd.notna(history_df["Volume"].sum())
                    else None
                ),
                "price_change": price_change,
                "price_change_percent": price_change_percent,
                "data_points": len(history_df),
            }
        else:
            logger.warning(
                f"Could not find valid start/end prices in history for {ticker}."
            )
            return {
                "error": f"Could not find valid price data points for {ticker} in the specified period."
            }

        serializable_summary = {k: v for k, v in summary.items()}
        logger.info(
            f"History summary calculated for {ticker} from {start_date} to {end_date}."
        )

        return {
            "ticker": ticker,
            "summary": serializable_summary,
            "requested_start_date": start_date,
            "requested_end_date": end_date,
            "interval": interval,
            "message": f"Summary of historical data for {ticker} from {summary.get('period_start_date')} to {summary.get('period_end_date')} calculated.",
        }

    except Exception as e:
        logger.exception(f"Error processing history for {ticker}: {e}")
        return {"error": f"Error processing history for {ticker}: {str(e)}"}


def get_company_info(
    ticker: str, data_vendor: str = "yfinance", api_key: Optional[str] = None
) -> Dict[str, Any]:
    try:
        vendor = DataVendorFactory.get_vendor(vendor_name=data_vendor, api_key=api_key)
        company_info_series = vendor.get_company_info(ticker=ticker)

        if company_info_series is None or company_info_series.empty:
            logger.warning(f"No company information returned by vendor for {ticker}.")
            return {"error": f"No company information found for {ticker}."}

        info_dict = company_info_series.to_dict()
        cleaned_info = {}
        keys_to_include = [
            "longName",
            "symbol",
            "sector",
            "industry",
            "country",
            "website",
            "longBusinessSummary",
            "fullTimeEmployees",
            "marketCap",
            "trailingPE",
            "forwardPE",
            "dividendYield",
            "beta",
            "fiftyTwoWeekHigh",
            "fiftyTwoWeekLow",
        ]
        for key in keys_to_include:
            if key in info_dict and pd.notna(info_dict[key]):
                value = info_dict[key]
                # Use safe_float for numbers, otherwise convert to string
                cleaned_info[key] = (
                    safe_float(value)
                    if isinstance(value, (int, float, np.number))
                    else str(value)
                )

        if not cleaned_info.get("longName") and not cleaned_info.get("symbol"):
            logger.warning(
                f"Company info for {ticker} lacks essential fields (name/symbol)."
            )
            # Decide if this constitutes an error or just incomplete data
            # return {"error": f"Incomplete company information received for {ticker}."}

        logger.info(f"Company info processed for {ticker}.")
        return {"ticker": ticker, "company_info": cleaned_info}
    except Exception as e:
        logger.exception(f"Error fetching company info for {ticker}: {e}")
        return {"error": f"Error fetching company info for {ticker}: {str(e)}"}


def get_institutional_investors(
    ticker: str,
    data_vendor: str = "yfinance",
    api_key: Optional[str] = None,
    limit: int = 5,
) -> Dict[str, Any]:
    try:
        vendor = DataVendorFactory.get_vendor(vendor_name=data_vendor, api_key=api_key)
        institutional_investors_df = vendor.get_institutional_holders(ticker=ticker)

        if institutional_investors_df is None or institutional_investors_df.empty:
            logger.warning(f"No institutional investors data returned for {ticker}.")
            return {"error": f"No institutional investors data found for {ticker}."}

        institutional_investors_df = institutional_investors_df.head(limit)
        institutional_investors_records = institutional_investors_df.to_dict(
            orient="records"
        )

        cleaned_investors = []
        for investor in institutional_investors_records:
            cleaned_record = {}
            for k, v in investor.items():
                if pd.notna(v):
                    # Format 'Date Reported' if it's a timestamp
                    if k == "Date Reported" and isinstance(v, pd.Timestamp):
                        cleaned_record[k] = v.strftime("%Y-%m-%d")
                    # Format '% Out' as percentage string
                    elif k == "% Out" and isinstance(v, (float, np.number)):
                        cleaned_record[k] = (
                            f"{safe_float(v * 100):.2f}%" if v is not None else None
                        )
                    # Use safe_float for other numbers, else string
                    elif isinstance(v, (int, float, np.number)):
                        cleaned_record[k] = safe_float(v)
                    else:
                        cleaned_record[k] = str(v)
            # Filter out records that became empty after cleaning NaNs
            if cleaned_record:
                cleaned_investors.append(cleaned_record)

        if not cleaned_investors:
            logger.warning(
                f"Institutional investors data for {ticker} was empty after cleaning."
            )
            return {
                "error": f"No valid institutional investors data found for {ticker} after processing."
            }

        logger.info(
            f"Processed top {len(cleaned_investors)} institutional investors for {ticker}."
        )
        return {
            "ticker": ticker,
            "top_institutional_investors": cleaned_investors,
            "message": f"Top {len(cleaned_investors)} institutional investors provided.",
        }
    except Exception as e:
        logger.exception(f"Error fetching institutional investors for {ticker}: {e}")
        return {
            "error": f"Error fetching institutional investors for {ticker}: {str(e)}"
        }


def get_sec_filings(
    ticker: str,
    data_vendor: str = "yfinance",
    api_key: Optional[str] = None,
    filing_type: Optional[str] = None,
    limit: int = 5,  # Keep limit parameter here
) -> Dict[str, Any]:
    try:
        vendor = DataVendorFactory.get_vendor(vendor_name=data_vendor, api_key=api_key)
        # Fetch ALL filings from the vendor first
        all_sec_filings_list = vendor.get_sec_filings(
            ticker=ticker
        )  # Assumes vendor returns list of dicts

        if not all_sec_filings_list:
            logger.warning(f"No SEC filings data returned by vendor for {ticker}.")
            # Return error consistent with schema/expectations
            return {"error": f"No SEC filings data found for {ticker}."}

        filtered_filings = []
        count = 0
        for filing in all_sec_filings_list:  # Iterate through the fetched list
            # Normalize form type from vendor if necessary (e.g., 'Form 10-K')
            form_type_raw = filing.get(
                "form", filing.get("type", filing.get("form_type"))
            )  # Check common keys
            if not form_type_raw:
                continue  # Skip if no type identified

            form_type = (
                str(form_type_raw).upper().replace("FORM ", "")
            )  # Basic normalization

            # Apply filing_type filter if provided
            if filing_type and form_type != filing_type.upper():
                continue

            # Try to extract and format date robustly
            date_raw = filing.get(
                "filingDate", filing.get("date", filing.get("reportDate"))
            )  # Check common keys
            filing_date_str = None
            if isinstance(
                date_raw, (datetime, pd.Timestamp)
            ):  # Handle both datetime and pandas Timestamp
                filing_date_str = date_raw.strftime("%Y-%m-%d")
            elif isinstance(date_raw, str):
                try:  # Attempt to parse common formats
                    filing_date_str = pd.to_datetime(date_raw).strftime("%Y-%m-%d")
                except (ValueError, TypeError):
                    filing_date_str = date_raw  # Keep original string if parsing fails
            elif date_raw is not None:
                filing_date_str = str(date_raw)

            cleaned_filing = {
                "date": filing_date_str,
                "form_type": form_type,
                "description": filing.get("description", filing.get("title")),
                "link": filing.get(
                    "link", filing.get("url", filing.get("edgarUrl"))
                ),  # Check common keys
            }
            # Keep only non-None values
            filtered_filings.append(
                {k: v for k, v in cleaned_filing.items() if v is not None}
            )
            count += 1
            # Apply the limit HERE
            if count >= limit:
                break

        if not filtered_filings:
            filing_type_msg = f" of type {filing_type}" if filing_type else ""
            logger.warning(
                f"No SEC filings{filing_type_msg} found for {ticker} after filtering."
            )
            return {
                "error": f"No recent SEC filings{filing_type_msg} found for {ticker} matching the criteria."
            }

        logger.info(
            f"Found {len(filtered_filings)} SEC filings for {ticker}{f' of type {filing_type}' if filing_type else ''} (limit was {limit})."
        )
        return {
            "ticker": ticker,
            "sec_filings": filtered_filings,  # Return the limited list
            "message": f"Found {len(filtered_filings)} SEC filings{f' of type {filing_type}' if filing_type else ''}.",
        }

    except Exception as e:
        logger.exception(
            f"Error processing SEC filings for {ticker} in functionTool: {e}"
        )
        return {
            "error": f"Error fetching/processing SEC filings for {ticker}: {str(e)}"
        }


def get_financial_statements(
    ticker: str,
    data_vendor: str = "yfinance",
    api_key: Optional[str] = None,
    statement_type: str = "income_statement",
    period: str = "annual",
) -> Dict[str, Any]:
    try:
        vendor = DataVendorFactory.get_vendor(vendor_name=data_vendor, api_key=api_key)
        financial_statements_df = vendor.get_financial_statements(
            ticker=ticker, statement_type=statement_type, period=period
        )

        if financial_statements_df is None or financial_statements_df.empty:
            logger.warning(f"No {period} {statement_type} data returned for {ticker}.")
            return {"error": f"No {period} {statement_type} data found for {ticker}."}

        # Get the latest 2 available periods (columns are usually dates)
        latest_periods_cols = financial_statements_df.columns[:2]
        summary_data_df = financial_statements_df[latest_periods_cols]

        key_metrics_map = {
            "income_statement": [
                "Total Revenue",
                "Net Income",
                "Gross Profit",
                "Operating Income",
                "Basic EPS",
                "EBITDA",
            ],
            "balance_sheet": [
                "Total Assets",
                "Total Liabilities Net Minority Interest",
                "Total Equity Gross Minority Interest",
                "Total Debt",
                "Cash And Cash Equivalents",
            ],
            "cash_flow_statement": [
                "Free Cash Flow",
                "Operating Cash Flow",
                "Capital Expenditure",
                "Net Income",
            ],  # Added Net Income here too
        }

        # Filter for rows that exist in the dataframe, case-insensitive if needed
        available_rows = summary_data_df.index
        relevant_rows = [
            row
            for row in key_metrics_map.get(statement_type, [])
            if row in available_rows
        ]
        if not relevant_rows:
            logger.warning(
                f"None of the key metrics for {statement_type} found in the data for {ticker}."
            )
            return {
                "error": f"Key metrics for {statement_type} not found for {ticker}."
            }

        key_data_subset_df = summary_data_df.loc[relevant_rows]

        # Convert to dictionary, handling NaN/NaT and formatting
        key_data_dict = {}
        for col in key_data_subset_df.columns:
            col_date_str = (
                str(col.date()) if isinstance(col, pd.Timestamp) else str(col)
            )
            metrics = {}
            for idx, value in key_data_subset_df[col].items():
                metrics[idx] = (
                    safe_float(value) if pd.notna(value) else None
                )  # Use safe_float for numbers, None for NaN
            key_data_dict[col_date_str] = metrics

        logger.info(
            f"Financial statement summary created for {ticker}, type: {statement_type}, period: {period}."
        )
        return {
            "ticker": ticker,
            "statement_type": statement_type,
            "period": period,
            "latest_periods_summary": key_data_dict,
            "message": f"Key metrics from the latest {len(latest_periods_cols)} periods of the {statement_type} ({period}) provided.",
        }

    except Exception as e:
        logger.exception(f"Error processing financial statements for {ticker}: {e}")
        return {
            "error": f"Error processing financial statements for {ticker}: {str(e)}"
        }


def get_financial_news(
    ticker: str,
    data_vendor: str = "yfinance",
    api_key: Optional[str] = None,
    limit: int = 3,
) -> Dict[str, Any]:
    try:
        vendor = DataVendorFactory.get_vendor(vendor_name=data_vendor, api_key=api_key)
        news_list = vendor.get_news(ticker=ticker)  # Assumes returns list of dicts

        if not news_list:
            logger.warning(f"No news returned by vendor for {ticker}.")
            return {"error": f"No news found for {ticker}."}

        processed_news = []
        for item in news_list[:limit]:
            publish_time_ts = item.get("providerPublishTime")
            publish_time_str = None
            if publish_time_ts:
                try:
                    # Check if it's already datetime or needs conversion from timestamp
                    if isinstance(publish_time_ts, datetime):
                        publish_time_str = publish_time_ts.strftime("%Y-%m-%d %H:%M:%S")
                    else:  # Assume it's a timestamp (seconds)
                        publish_time_str = datetime.fromtimestamp(
                            int(publish_time_ts)
                        ).strftime("%Y-%m-%d %H:%M:%S")
                except (ValueError, TypeError):
                    publish_time_str = str(publish_time_ts)  # Fallback to string

            cleaned_item = {
                "title": item.get("title"),
                "publisher": item.get("publisher"),
                "link": item.get("link"),
                "publish_time": publish_time_str,
            }
            processed_news.append(
                {k: v for k, v in cleaned_item.items() if v is not None}
            )

        if not processed_news:
            logger.warning(f"News list for {ticker} was empty after processing.")
            return {
                "error": f"No valid news items found for {ticker} after processing."
            }

        logger.info(f"Processed {len(processed_news)} news items for {ticker}.")
        return {
            "ticker": ticker,
            "news": processed_news,
            "message": f"Top {len(processed_news)} news items provided.",
        }
    except Exception as e:
        logger.exception(f"Error fetching news for {ticker}: {e}")
        return {"error": f"Error fetching news for {ticker}: {str(e)}"}


def calculate_price_trend(
    ticker: str,
    data_vendor: str = "yfinance",
    api_key: Optional[str] = None,
    window1: int = 50,
    window2: int = 200,
) -> Dict[str, Any]:
    try:
        vendor = DataVendorFactory.get_vendor(vendor_name=data_vendor, api_key=api_key)

        # Fetch significantly more data to account for non-trading days
        # Roughly 1.5 years should be safe for a 200-day SMA (200 trading days ~ 280 calendar days)
        # Let's fetch around 400 calendar days as a buffer.
        days_to_fetch = max(window1, window2) + 200  # Increased buffer substantially
        end_date_dt = datetime.today()
        # Ensure start_date is calculated correctly
        start_date_dt = end_date_dt - timedelta(days=days_to_fetch)

        end_date = end_date_dt.strftime("%Y-%m-%d")
        start_date = start_date_dt.strftime("%Y-%m-%d")
        logger.info(
            f"Fetching data for trend calculation ({ticker}) from {start_date} to {end_date}"
        )

        history_df = vendor.get_prices(
            ticker=ticker, start_date=start_date, end_date=end_date, interval="day"
        )

        # Check *after* fetching if we have enough data points
        required_points = max(window1, window2)
        if history_df.empty or len(history_df) < required_points:
            logger.warning(
                f"Insufficient historical data points ({len(history_df)}) fetched for {ticker} to calculate {required_points}-day trend, even after requesting {days_to_fetch} calendar days."
            )
            # Provide a more informative error
            return {
                "error": f"Insufficient historical data for {ticker} to calculate {required_points}-day trend (received {len(history_df)} points). Try a shorter long-term window if applicable."
            }

        # --- Calculation logic remains the same ---
        if "Close" not in history_df.columns:
            logger.error(f"'Close' column not found in history data for {ticker}.")
            return {"error": f"Price data format error for {ticker}."}

        history_df[f"SMA{window1}"] = (
            history_df["Close"].rolling(window=window1, min_periods=window1).mean()
        )  # Ensure full window for SMA
        history_df[f"SMA{window2}"] = (
            history_df["Close"].rolling(window=window2, min_periods=window2).mean()
        )  # Ensure full window for SMA

        # Drop rows with NaN SMAs before getting the latest valid data
        valid_trend_data = history_df.dropna(subset=[f"SMA{window1}", f"SMA{window2}"])

        if valid_trend_data.empty:
            logger.warning(
                f"Could not calculate SMAs for {ticker}, possibly due to gaps in data near the end."
            )
            return {
                "error": f"Could not calculate trend for {ticker}, possibly due to recent data gaps."
            }

        latest_data = valid_trend_data.iloc[-1]  # Use last row with valid SMAs
        current_price = safe_float(latest_data["Close"])
        sma_short = safe_float(latest_data[f"SMA{window1}"])
        sma_long = safe_float(latest_data[f"SMA{window2}"])
        # --- End calculation logic ---

        trend_signal = "Indeterminate"
        if current_price is not None and sma_short is not None and sma_long is not None:
            # Trend logic remains the same
            if current_price > sma_short > sma_long:
                trend_signal = f"Strong Uptrend (Price > SMA{window1} > SMA{window2})"
            elif sma_short > current_price > sma_long:
                trend_signal = f"Potential Uptrend/Correction Below SMA{window1} (SMA{window1} > Price > SMA{window2})"
            elif sma_long > current_price > sma_short:
                trend_signal = f"Potential Downtrend/Rally Below SMA{window2} (SMA{window2} > Price > SMA{window1})"
            elif sma_short > sma_long > current_price:
                trend_signal = f"Strong Downtrend (Price < SMA{window2} < SMA{window1})"
            elif sma_long > sma_short > current_price:
                trend_signal = f"Strong Downtrend (Price < SMA{window1} < SMA{window2})"
            elif current_price > sma_long > sma_short:
                trend_signal = f"Potential Uptrend/Consolidation Above SMA{window2} (Price > SMA{window2} > SMA{window1})"
            elif (
                abs(current_price - sma_short) < 0.005 * current_price
                or abs(current_price - sma_long) < 0.005 * current_price
            ):  # Check if price is very close to SMA
                trend_signal = f"Price Testing SMA(s)"
            else:
                trend_signal = "Neutral / Sideways"
        else:
            logger.warning(
                f"Could not determine trend for {ticker} due to missing price/SMA values in final calculation."
            )

        result = {
            "ticker": ticker,
            "current_price": current_price,
            f"sma_{window1}_day": sma_short,
            f"sma_{window2}_day": sma_long,
            "trend_signal": trend_signal,
            "message": f"Trend analysis based on {window1}-day and {window2}-day SMAs calculated.",
        }
        logger.info(f"Trend calculated for {ticker}: {trend_signal}")
        return result

    except Exception as e:
        logger.exception(f"Error calculating trend for {ticker}: {e}")
        return {"error": f"Error calculating trend for {ticker}: {str(e)}"}


def calculate_period_statistics(
    ticker: str,
    data_vendor: str = "yfinance",
    api_key: Optional[str] = None,
    start_date: str = None,
    end_date: str = None,
    # interval: str = "day" # Using daily data implicitly for common stats
) -> Dict[str, Any]:
    try:
        vendor = DataVendorFactory.get_vendor(vendor_name=data_vendor, api_key=api_key)

        if not start_date or not end_date:
            today = datetime.today()
            end_date_dt = today
            start_date_dt = today - timedelta(days=365)  # Default to 1 year
            end_date = end_date_dt.strftime("%Y-%m-%d")
            start_date = start_date_dt.strftime("%Y-%m-%d")
            logger.info(
                f"Defaulting statistics period for {ticker} to: {start_date} - {end_date}"
            )

        history_df = vendor.get_prices(
            ticker=ticker,
            start_date=start_date,
            end_date=end_date,
            interval="day",  # Use daily interval for stats
        )

        if history_df.empty:
            logger.warning(
                f"No historical data found for {ticker} between {start_date} and {end_date}."
            )
            return {
                "error": f"No historical data found for {ticker} between {start_date} and {end_date}."
            }

        close_prices = history_df["Close"].dropna()

        if close_prices.empty:
            logger.warning(
                f"No valid closing prices found for {ticker} in the period {start_date}-{end_date}."
            )
            return {
                "error": f"No valid closing prices found for {ticker} in the period."
            }

        mean_price = safe_float(close_prices.mean())
        median_price = safe_float(close_prices.median())
        std_dev = safe_float(close_prices.std())

        volatility_percent = None
        if mean_price is not None and mean_price != 0 and std_dev is not None:
            volatility_percent = safe_float((std_dev / mean_price) * 100)

        min_price = safe_float(close_prices.min())
        max_price = safe_float(close_prices.max())

        result = {
            "ticker": ticker,
            "start_date": start_date,
            "end_date": end_date,
            "mean_price": mean_price,
            "median_price": median_price,
            "standard_deviation": std_dev,
            "volatility_percent": volatility_percent,  # Often expressed as percentage of mean
            "minimum_price": min_price,
            "maximum_price": max_price,
            "message": f"Statistical analysis for the period {start_date} to {end_date} calculated.",
        }
        logger.info(f"Statistics calculated for {ticker} ({start_date} to {end_date}).")
        return result

    except Exception as e:
        logger.exception(f"Error calculating statistics for {ticker}: {e}")
        return {"error": f"Error calculating statistics for {ticker}: {str(e)}"}


def calculate_returns(
    ticker: str,
    data_vendor: str = "yfinance",
    api_key: Optional[str] = None,
    start_date: str = None,
    end_date: str = None,
    # interval: str = "day" # Implicitly daily for standard return calcs
) -> Dict[str, Any]:
    try:
        vendor = DataVendorFactory.get_vendor(vendor_name=data_vendor, api_key=api_key)

        if not start_date or not end_date:
            today = datetime.today()
            end_date_dt = today
            start_date_dt = today - timedelta(days=365)  # Default to 1 year
            end_date = end_date_dt.strftime("%Y-%m-%d")
            start_date = start_date_dt.strftime("%Y-%m-%d")
            logger.info(
                f"Defaulting returns period for {ticker} to: {start_date} - {end_date}"
            )

        # Fetch only start and end points if possible, else full history
        # Optimization: Fetch minimal data if vendor supports it. yfinance needs range.
        history_df = vendor.get_prices(
            ticker=ticker, start_date=start_date, end_date=end_date, interval="day"
        )

        if history_df.empty or len(history_df) < 2:
            logger.warning(
                f"Insufficient historical data ({len(history_df)} points) for {ticker} between {start_date} and {end_date} to calculate returns."
            )
            return {
                "error": f"Insufficient historical data for {ticker} between {start_date} and {end_date} to calculate returns."
            }

        # Find first and last valid closing prices in the *returned* data range
        close_prices = history_df["Close"].dropna()
        if len(close_prices) < 2:
            logger.warning(
                f"Not enough valid closing prices ({len(close_prices)}) found for return calculation for {ticker}."
            )
            return {
                "error": f"Could not find at least two valid closing prices for {ticker} in the period."
            }

        period_start_price = safe_float(close_prices.iloc[0])
        period_end_price = safe_float(close_prices.iloc[-1])
        actual_start_date = close_prices.index[0].strftime("%Y-%m-%d")
        actual_end_date = close_prices.index[-1].strftime("%Y-%m-%d")

        if period_start_price is None or period_start_price == 0:
            logger.error(
                f"Invalid starting price ({period_start_price}) for return calculation for {ticker} on {actual_start_date}."
            )
            return {
                "error": f"Invalid starting price ({period_start_price}) on {actual_start_date} for return calculation."
            }
        if period_end_price is None:
            logger.error(
                f"Invalid ending price ({period_end_price}) for return calculation for {ticker} on {actual_end_date}."
            )
            return {
                "error": f"Invalid ending price ({period_end_price}) on {actual_end_date} for return calculation."
            }

        total_return_percent = safe_float(
            ((period_end_price - period_start_price) / period_start_price) * 100
        )

        annualized_return_percent = None
        try:
            start_dt = pd.to_datetime(actual_start_date)
            end_dt = pd.to_datetime(actual_end_date)
            days_in_period = (end_dt - start_dt).days
            # Avoid division by zero or calculating for same day
            if days_in_period > 0:
                years_in_period = days_in_period / 365.25
                if total_return_percent is not None:
                    # Ensure base for exponentiation is non-negative
                    base = 1 + (total_return_percent / 100)
                    if base >= 0:
                        annualized_return_percent = safe_float(
                            ((base) ** (1 / years_in_period) - 1) * 100
                        )
                    else:
                        logger.warning(
                            f"Cannot calculate annualized return for {ticker} due to negative base ({base}). Total return was {total_return_percent}%."
                        )

        except Exception as calc_e:
            logger.error(f"Error calculating annualized return for {ticker}: {calc_e}")
            annualized_return_percent = None  # Ensure it's None on error

        result = {
            "ticker": ticker,
            "start_date_used": actual_start_date,  # Report actual dates used
            "end_date_used": actual_end_date,
            "start_price": period_start_price,
            "end_price": period_end_price,
            "total_return_percent": total_return_percent,
            "annualized_return_percent": annualized_return_percent,
            "message": f"Return calculation from {actual_start_date} to {actual_end_date} completed.",
        }
        logger.info(
            f"Returns calculated for {ticker} ({actual_start_date} to {actual_end_date})."
        )
        return result

    except Exception as e:
        logger.exception(f"Error calculating returns for {ticker}: {e}")
        return {"error": f"Error calculating returns for {ticker}: {str(e)}"}
