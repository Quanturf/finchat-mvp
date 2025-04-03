from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field
from .api import chat
import yfinance as yf
import pandas as pd
import logging
from datetime import datetime

from .dataVendors import functionTool

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="QuantAI Finance Chatbot",
    version="0.1.0",
    description="API for the QuantAI financial chatbot, providing chat interface and direct data endpoints.",
)

origins = [
    "http://localhost:5173",
    "http://localhost:3000",
    "http://127.0.0.1:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(chat.chatRouter, prefix="/chat", tags=["Chat"])


@app.get("/health", tags=["System"])
async def health():
    return {"status": "ok", "timestamp": datetime.utcnow().isoformat()}


@app.get("/", tags=["System"])
async def root():
    return {"message": "Welcome to the QuantAI Finance Chatbot API!"}


# --- Direct Data Endpoint Models (Pydantic) ---


class CompanyOfficer(BaseModel):
    maxAge: Optional[int] = 1
    name: Optional[str] = None
    age: Optional[int] = None
    title: Optional[str] = None
    yearBorn: Optional[int] = None
    fiscalYear: Optional[int] = None
    totalPay: Optional[float] = None  # Use float for currency
    exercisedValue: Optional[float] = None
    unexercisedValue: Optional[float] = None


class CompanyInfo(BaseModel):
    symbol: str
    longName: Optional[str] = None
    address1: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    zip: Optional[str] = None
    country: Optional[str] = None
    phone: Optional[str] = None
    website: Optional[str] = None
    industry: Optional[str] = None
    industryKey: Optional[str] = None
    industryDisp: Optional[str] = None
    sector: Optional[str] = None
    sectorKey: Optional[str] = None
    sectorDisp: Optional[str] = None
    longBusinessSummary: Optional[str] = None
    fullTimeEmployees: Optional[int] = None
    companyOfficers: List[CompanyOfficer] = Field(default_factory=list)
    auditRisk: Optional[int] = None
    boardRisk: Optional[int] = None
    compensationRisk: Optional[int] = None
    shareHolderRightsRisk: Optional[int] = None
    overallRisk: Optional[int] = None
    governanceEpochDate: Optional[int] = None
    compensationAsOfEpochDate: Optional[int] = None
    maxAge: Optional[int] = None
    priceHint: Optional[int] = None
    previousClose: Optional[float] = None
    open: Optional[float] = None
    dayLow: Optional[float] = None
    dayHigh: Optional[float] = None
    regularMarketPreviousClose: Optional[float] = None
    regularMarketOpen: Optional[float] = None
    regularMarketDayLow: Optional[float] = None
    regularMarketDayHigh: Optional[float] = None
    dividendRate: Optional[float] = None
    dividendYield: Optional[float] = None
    exDividendDate: Optional[int] = None  # Consider converting to date string
    payoutRatio: Optional[float] = None
    fiveYearAvgDividendYield: Optional[float] = None
    beta: Optional[float] = None
    trailingPE: Optional[float] = None
    forwardPE: Optional[float] = None
    volume: Optional[int] = None
    regularMarketVolume: Optional[int] = None
    averageVolume: Optional[int] = None
    averageVolume10days: Optional[int] = None
    averageDailyVolume10Day: Optional[int] = None
    bid: Optional[float] = None
    ask: Optional[float] = None
    bidSize: Optional[int] = None
    askSize: Optional[int] = None
    marketCap: Optional[float] = None  # Use float for large numbers
    fiftyTwoWeekLow: Optional[float] = None
    fiftyTwoWeekHigh: Optional[float] = None
    priceToSalesTrailing12Months: Optional[float] = None
    fiftyDayAverage: Optional[float] = None
    twoHundredDayAverage: Optional[float] = None
    trailingAnnualDividendRate: Optional[float] = None
    trailingAnnualDividendYield: Optional[float] = None
    currency: Optional[str] = None
    enterpriseValue: Optional[float] = None
    profitMargins: Optional[float] = None
    floatShares: Optional[float] = None
    sharesOutstanding: Optional[float] = None
    sharesShort: Optional[float] = None
    sharesShortPriorMonth: Optional[float] = None
    sharesShortPreviousMonthDate: Optional[int] = None
    dateShortInterest: Optional[int] = None
    sharesPercentSharesOut: Optional[float] = None
    heldPercentInsiders: Optional[float] = None
    heldPercentInstitutions: Optional[float] = None
    shortRatio: Optional[float] = None
    shortPercentOfFloat: Optional[float] = None
    impliedSharesOutstanding: Optional[float] = None
    bookValue: Optional[float] = None
    priceToBook: Optional[float] = None
    lastFiscalYearEnd: Optional[int] = None
    nextFiscalYearEnd: Optional[int] = None
    mostRecentQuarter: Optional[int] = None
    earningsQuarterlyGrowth: Optional[float] = None
    netIncomeToCommon: Optional[float] = None
    trailingEps: Optional[float] = None
    forwardEps: Optional[float] = None
    pegRatio: Optional[float] = None
    lastSplitFactor: Optional[str] = None
    lastSplitDate: Optional[int] = None
    enterpriseToRevenue: Optional[float] = None
    enterpriseToEbitda: Optional[float] = None
    # fiftyTwoWeekChange: Optional[float] = None # Often causes issues
    # SandP52WeekChange: Optional[float] = Field(None, alias="SandP52WeekChange") # Often causes issues
    lastDividendValue: Optional[float] = None
    lastDividendDate: Optional[int] = None
    # Core financial metrics
    currentPrice: Optional[float] = None
    targetHighPrice: Optional[float] = None
    targetLowPrice: Optional[float] = None
    targetMeanPrice: Optional[float] = None
    targetMedianPrice: Optional[float] = None
    recommendationMean: Optional[float] = None
    recommendationKey: Optional[str] = None
    numberOfAnalystOpinions: Optional[int] = None
    totalCash: Optional[float] = None
    totalCashPerShare: Optional[float] = None
    ebitda: Optional[float] = None
    totalDebt: Optional[float] = None
    quickRatio: Optional[float] = None
    currentRatio: Optional[float] = None
    totalRevenue: Optional[float] = None
    debtToEquity: Optional[float] = None
    revenuePerShare: Optional[float] = None
    returnOnAssets: Optional[float] = None
    returnOnEquity: Optional[float] = None
    grossProfits: Optional[float] = None
    freeCashflow: Optional[float] = None
    operatingCashflow: Optional[float] = None
    earningsGrowth: Optional[float] = None
    revenueGrowth: Optional[float] = None
    grossMargins: Optional[float] = None
    ebitdaMargins: Optional[float] = None
    operatingMargins: Optional[float] = None
    financialCurrency: Optional[str] = None
    trailingPegRatio: Optional[float] = None

    class Config:
        # Allow extra fields from yfinance Ticker.info() without error
        # Use 'ignore' if you don't want them, 'allow' to include them if they exist
        extra = "ignore"
        # Ensure NaN/Infinity are handled, e.g., by coercing to None or string
        # This might require custom serializers if Pydantic default isn't enough
        # Pydantic v2 handles NaN/Infinity better, often converting to None by default


# --- Direct Data Endpoints ---


@app.get(
    "/company_info/{ticker}", response_model=CompanyInfo, tags=["Direct Data - Company"]
)
async def get_company_info_direct(ticker: str):
    try:
        company = yf.Ticker(ticker)
        info = company.info
        if not info or not info.get("symbol"):
            raise HTTPException(
                status_code=404, detail=f"No data found for ticker: {ticker}"
            )

        # Clean officers data before validating with Pydantic model
        raw_officers = info.get("companyOfficers", [])
        valid_officers = []
        if isinstance(raw_officers, list):
            for officer_data in raw_officers:
                if isinstance(officer_data, dict):
                    # Coerce numeric fields that might be missing or NaN
                    for field in [
                        "age",
                        "yearBorn",
                        "fiscalYear",
                        "totalPay",
                        "exercisedValue",
                        "unexercisedValue",
                    ]:
                        if field in officer_data and not isinstance(
                            officer_data[field], (int, float)
                        ):
                            try:
                                officer_data[field] = float(officer_data[field])
                            except (ValueError, TypeError):
                                officer_data[field] = (
                                    None  # Set to None if conversion fails
                                )
                    try:
                        valid_officers.append(
                            CompanyOfficer(**officer_data).model_dump(exclude_none=True)
                        )
                    except Exception as officer_exc:
                        logger.warning(
                            f"Skipping officer due to validation error for {ticker}: {officer_exc} - Data: {officer_data}"
                        )
                else:
                    logger.warning(
                        f"Skipping invalid officer data structure for {ticker}: {officer_data}"
                    )
        info["companyOfficers"] = valid_officers

        # Handle potential NaN/Infinity before creating the main CompanyInfo model
        cleaned_info = {}
        for key, value in info.items():
            if isinstance(value, (float, int)):
                if pd.isna(value) or not pd.core.dtypes.common.is_number(
                    value
                ):  # More robust check
                    cleaned_info[key] = None
                else:
                    cleaned_info[key] = value
            else:
                cleaned_info[key] = (
                    value  # Keep non-numeric as is for Pydantic validation
                )

        # Ensure required 'symbol' is present
        if "symbol" not in cleaned_info:
            cleaned_info["symbol"] = ticker  # Add if missing

        return CompanyInfo(**cleaned_info)

    except HTTPException as http_exc:
        raise http_exc
    except Exception as e:
        logger.exception(f"Error fetching direct company info for {ticker}: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Internal server error fetching info for {ticker}: {str(e)}",
        )


class EarningsData(BaseModel):
    date: str
    epsActual: Optional[float] = None
    epsEstimate: Optional[float] = None
    epsDifference: Optional[float] = None
    surprisePercent: Optional[float] = None


@app.get(
    "/earnings/{ticker}",
    response_model=List[EarningsData],
    tags=["Direct Data - Financials"],
)
async def get_earnings_direct(
    ticker: str,
    limit: int = Query(
        4, description="Number of recent earnings periods to retrieve", ge=1, le=16
    ),
):
    try:
        company = yf.Ticker(ticker)
        earnings_history_df = company.earnings_history

        if earnings_history_df.empty:
            logger.warning(f"No earnings history found via yfinance for {ticker}")
            return []  # Return empty list if no data

        earnings_list = []
        # Take the latest 'limit' rows
        for index, row in earnings_history_df.tail(limit).iterrows():
            # Ensure index is timezone-naive string if it's a timestamp
            date_str = (
                str(index.date()) if isinstance(index, pd.Timestamp) else str(index)
            )

            # Safely get values, defaulting to None if key missing or value is NaN
            earnings_list.append(
                EarningsData(
                    date=date_str,
                    epsActual=(
                        row.get("EPS Actual")
                        if pd.notna(row.get("EPS Actual"))
                        else None
                    ),
                    epsEstimate=(
                        row.get("EPS Estimate")
                        if pd.notna(row.get("EPS Estimate"))
                        else None
                    ),
                    epsDifference=(
                        row.get("Difference")
                        if pd.notna(row.get("Difference"))
                        else None
                    ),
                    surprisePercent=(
                        row.get("Surprise(%)")
                        if pd.notna(row.get("Surprise(%)"))
                        else None
                    ),
                ).model_dump(exclude_none=True)
            )
        return earnings_list
    except Exception as e:
        logger.exception(f"Error fetching direct earnings for {ticker}: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Internal server error fetching earnings for {ticker}: {str(e)}",
        )


class FinancialStatementResponse(BaseModel):
    ticker: str
    statement_type: str
    period: str
    statement: Dict[str, Dict[str, Optional[float]]]  # Dates as keys, metrics as keys


@app.get(
    "/financial_statements/{ticker}",
    response_model=FinancialStatementResponse,
    tags=["Direct Data - Financials"],
)
async def get_financial_statements_direct(
    ticker: str,
    statement_type: str = Query(
        ...,
        description="Type of financial statement",
        enum=["income_statement", "balance_sheet", "cash_flow_statement"],
    ),
    period: str = Query("annual", description="Period", enum=["annual", "quarterly"]),
):
    try:
        company = yf.Ticker(ticker)
        statement_df = None

        if statement_type == "income_statement":
            statement_df = (
                company.income_stmt
                if period == "annual"
                else company.quarterly_income_stmt
            )
        elif statement_type == "balance_sheet":
            statement_df = (
                company.balance_sheet
                if period == "annual"
                else company.quarterly_balance_sheet
            )
        elif statement_type == "cash_flow_statement":
            statement_df = (
                company.cashflow if period == "annual" else company.quarterly_cashflow
            )

        if statement_df is None or statement_df.empty:
            raise HTTPException(
                status_code=404,
                detail=f"{period.capitalize()} {statement_type.replace('_', ' ')} not found for {ticker}",
            )

        # Convert DataFrame to the desired dictionary format, handling NaN/NaT
        statement_dict = {}
        for col in statement_df.columns:
            # Convert timestamp column to YYYY-MM-DD string
            col_date_str = (
                str(col.date()) if isinstance(col, pd.Timestamp) else str(col)
            )
            metrics = {}
            for idx, value in statement_df[col].items():
                metrics[str(idx)] = float(value) if pd.notna(value) else None
            statement_dict[col_date_str] = metrics

        return FinancialStatementResponse(
            ticker=ticker,
            statement_type=statement_type,
            period=period,
            statement=statement_dict,
        )

    except HTTPException as http_exc:
        raise http_exc
    except Exception as e:
        logger.exception(
            f"Error fetching direct financial statements for {ticker}: {e}"
        )
        raise HTTPException(
            status_code=500,
            detail=f"Internal server error fetching {statement_type} for {ticker}: {str(e)}",
        )


class SECFiling(BaseModel):
    date: Optional[str] = None
    form_type: Optional[str] = None
    link: Optional[str] = None
    description: Optional[str] = None


@app.get(
    "/sec_filings/{ticker}",
    response_model=List[SECFiling],
    tags=["Direct Data - Company"],
)
async def get_sec_filings_direct(
    ticker: str,
    filing_type: Optional[str] = Query(
        None,
        description="Filter by specific SEC filing type (e.g., 10-K, 10-Q, 8-K). Case insensitive.",
        enum=[
            "10-K",
            "10-Q",
            "8-K",
            "4",
            "13F",
            "S-1",
            "DEF 14A",
        ],
    ),
    limit: int = Query(
        10, description="Maximum number of recent filings to return", ge=1, le=50
    ),
):
    try:
        company = yf.Ticker(ticker)
        from .dataVendors.yfinance.vendor import (
            YahooFinance,
        )

        yfinance_vendor = YahooFinance()
        filings_list = yfinance_vendor.get_sec_filings(ticker=ticker)

        if not filings_list:
            logger.warning(f"No SEC filings returned via yfinance vendor for {ticker}")
            return []

        processed_filings = []
        count = 0
        for filing_data in filings_list:
            # Normalize form type if needed
            raw_form_type = filing_data.get(
                "type", filing_data.get("form", filing_data.get("form_type"))
            )  # Check common keys
            if not raw_form_type:
                continue
            current_form_type = str(raw_form_type).upper().replace("FORM ", "")

            if filing_type and current_form_type != filing_type.upper():
                continue

            # Format date
            date_raw = filing_data.get("date", filing_data.get("filingDate"))
            filing_date_str = None
            if isinstance(date_raw, datetime):
                filing_date_str = date_raw.strftime("%Y-%m-%d")
            elif isinstance(date_raw, str):
                try:
                    filing_date_str = pd.to_datetime(date_raw).strftime("%Y-%m-%d")
                except:
                    filing_date_str = date_raw  # keep as string if parse fails
            elif date_raw is not None:
                filing_date_str = str(date_raw)

            processed_filings.append(
                SECFiling(
                    date=filing_date_str,
                    form_type=current_form_type,
                    link=filing_data.get(
                        "edgarUrl", filing_data.get("link", filing_data.get("url"))
                    ),
                    description=filing_data.get(
                        "title", filing_data.get("description")
                    ),
                ).model_dump(exclude_none=True)
            )
            count += 1
            if count >= limit:
                break

        return processed_filings

    except Exception as e:
        logger.exception(f"Error fetching direct SEC filings for {ticker}: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Internal server error fetching SEC filings for {ticker}: {str(e)}",
        )


class FinancialMetric(BaseModel):
    metric_name: str
    value: Optional[Any] = None
    # value: Union[str, float, int, None] = None # More flexible type


@app.get(
    "/key_metrics/{ticker}",
    response_model=List[FinancialMetric],
    tags=["Direct Data - Financials"],
)
async def get_key_metrics_direct(ticker: str):
    try:
        company = yf.Ticker(ticker)
        info = company.info
        if not info or not info.get("symbol"):
            raise HTTPException(
                status_code=404, detail=f"No data found for ticker: {ticker}"
            )

        metrics_to_extract = {
            "Market Cap": "marketCap",
            "PE Ratio (TTM)": "trailingPE",
            "Forward PE": "forwardPE",
            "Dividend Yield": "dividendYield",
            "Beta": "beta",
            "52 Week High": "fiftyTwoWeekHigh",
            "52 Week Low": "fiftyTwoWeekLow",
            "Price to Book": "priceToBook",
            "Profit Margin": "profitMargins",
            "Revenue Growth (YoY)": "revenueGrowth",  # Note: yfinance might call this 'revenueQuarterlyGrowth' sometimes
            "Earnings Growth (YoY)": "earningsGrowth",  # Note: yfinance might call this 'earningsQuarterlyGrowth'
            "Return on Equity (ROE)": "returnOnEquity",
            "Debt to Equity": "debtToEquity",
        }

        metrics_list = []
        for name, key in metrics_to_extract.items():
            raw_value = info.get(key)
            value = None
            if pd.notna(raw_value):
                if isinstance(raw_value, (float, int)):
                    # Format percentages nicely
                    if key in [
                        "dividendYield",
                        "profitMargins",
                        "revenueGrowth",
                        "earningsGrowth",
                        "returnOnEquity",
                    ]:
                        value = f"{raw_value * 100:.2f}%"
                    # Format large numbers (Market Cap)
                    elif key == "marketCap":
                        if raw_value > 1_000_000_000_000:
                            value = f"${raw_value / 1_000_000_000_000:.2f}T"
                        elif raw_value > 1_000_000_000:
                            value = f"${raw_value / 1_000_000_000:.2f}B"
                        elif raw_value > 1_000_000:
                            value = f"${raw_value / 1_000_000:.2f}M"
                        else:
                            value = f"${raw_value:,.2f}"
                    # Default formatting for other numbers
                    else:
                        value = (
                            f"{raw_value:,.2f}"
                            if isinstance(raw_value, float)
                            else f"{raw_value:,}"
                        )
                else:
                    value = str(raw_value)  # Convert non-numeric to string

            metrics_list.append(FinancialMetric(metric_name=name, value=value))

        return metrics_list
    except HTTPException as http_exc:
        raise http_exc
    except Exception as e:
        logger.exception(f"Error fetching direct key metrics for {ticker}: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Internal server error fetching key metrics for {ticker}: {str(e)}",
        )


class HistoricalPriceData(BaseModel):
    date: str
    open: Optional[float] = None
    high: Optional[float] = None
    low: Optional[float] = None
    close: Optional[float] = None
    adj_close: Optional[float] = Field(None, alias="adjClose")
    volume: Optional[int] = None


@app.get(
    "/historical_prices/{ticker}",
    response_model=List[HistoricalPriceData],
    tags=["Direct Data - Prices"],
)
async def get_historical_prices_direct(
    ticker: str,
    start_date: str = Query(
        ..., description="Start date (YYYY-MM-DD)", pattern=r"^\d{4}-\d{2}-\d{2}$"
    ),
    end_date: str = Query(
        ..., description="End date (YYYY-MM-DD)", pattern=r"^\d{4}-\d{2}-\d{2}$"
    ),
    interval: str = Query("1d", description="Interval", enum=["1d", "1wk", "1mo"]),
):
    try:
        start_dt = datetime.strptime(start_date, "%Y-%m-%d")
        end_dt = datetime.strptime(end_date, "%Y-%m-%d")

        if start_dt > end_dt:
            logger.error(
                f"Invalid date range requested for {ticker}: start_date ({start_date}) is after end_date ({end_date})"
            )
            raise HTTPException(
                status_code=400,
                detail=f"Invalid date range: start_date ({start_date}) cannot be after end_date ({end_date}).",
            )
    except ValueError as date_err:
        logger.error(f"Invalid date format provided: {date_err}")
        raise HTTPException(
            status_code=400,
            detail=f"Invalid date format. Please use YYYY-MM-DD. Error: {date_err}",
        )

    try:
        company = yf.Ticker(ticker)
        history = company.history(start=start_date, end=end_date, interval=interval)

        if history.empty:
            logger.warning(
                f"No historical price data found via yfinance for {ticker} in range {start_date}-{end_date} (interval: {interval})"
            )
            return []

        prices = []
        for index, row in history.iterrows():
            date_str = (
                str(index.date()) if isinstance(index, pd.Timestamp) else str(index)
            )
            prices.append(
                HistoricalPriceData(
                    date=date_str,
                    open=row.get("Open") if pd.notna(row.get("Open")) else None,
                    high=row.get("High") if pd.notna(row.get("High")) else None,
                    low=row.get("Low") if pd.notna(row.get("Low")) else None,
                    close=row.get("Close") if pd.notna(row.get("Close")) else None,
                    adjClose=(
                        row.get("Adj Close")
                        if pd.notna(row.get("Adj Close"))
                        else row.get("Close") if pd.notna(row.get("Close")) else None
                    ),
                    volume=int(row["Volume"]) if pd.notna(row.get("Volume")) else None,
                ).model_dump(exclude_none=True, by_alias=True)
            )
        return prices
    except HTTPException as http_exc:
        raise http_exc
    except Exception as e:
        logger.exception(
            f"Error fetching direct historical prices for {ticker} ({start_date} to {end_date}): {e}"
        )
        raise HTTPException(
            status_code=500,
            detail=f"Internal server error fetching historical prices for {ticker}: {str(e)}",
        )


class NewsItem(BaseModel):
    title: str
    publisher: str
    link: str
    publish_time: Optional[str] = None
    summary: Optional[str] = None
    description: Optional[str] = None


@app.get("/news/{ticker}", response_model=List[NewsItem], tags=["Direct Data - News"])
async def get_news_direct(
    ticker: str,
    limit: int = Query(
        10, description="Maximum number of news articles to retrieve", ge=1, le=30
    ),
):
    try:
        company = yf.Ticker(ticker)
        from .dataVendors.yfinance.vendor import YahooFinance

        yfinance_vendor = YahooFinance()
        news_list_raw = yfinance_vendor.get_news(ticker=ticker)

        if not news_list_raw:
            logger.warning(f"No news found via yfinance vendor for {ticker}")
            return []

        news_items = []
        for item in news_list_raw[:limit]:
            item = item.get("content")
            publish_time_ts = item.get("pubDate")
            publish_time_str = None
            if publish_time_ts:
                try:
                    publish_time_str = datetime.fromtimestamp(
                        int(publish_time_ts)
                    ).strftime("%Y-%m-%d %H:%M:%S")
                except (ValueError, TypeError):
                    publish_time_str = str(publish_time_ts)

            title = item.get("title")
            link = item.get("canonicalUrl").get("url")
            publisher = item.get("provider").get("displayName")
            summary = item.get("summary")
            description = item.get("description")
            if title and link and publisher:
                news_items.append(
                    NewsItem(
                        title=title,
                        publisher=publisher,
                        link=link,
                        publish_time=publish_time_str,
                        summary=summary,
                        description=description,
                    ).model_dump(exclude_none=True)
                )

        return news_items
    except Exception as e:
        logger.exception(f"Error fetching direct news for {ticker}: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Internal server error fetching news for {ticker}: {str(e)}",
        )


class InstitutionalHolder(BaseModel):
    holder: str
    shares: int
    date_reported: str  # YYYY-MM-DD format
    percent_out: Optional[str] = Field(
        None, alias="percentOut"
    )  # Formatted string like "1.23%"
    value: Optional[float] = None  # Market value of holding


@app.get(
    "/institutional_holders/{ticker}",
    response_model=List[InstitutionalHolder],
    tags=["Direct Data - Company"],
)
async def get_institutional_holders_direct(
    ticker: str,
    limit: int = Query(
        10, description="Maximum number of top holders to retrieve", ge=1, le=50
    ),
):
    try:
        company = yf.Ticker(ticker)
        holders_df = company.institutional_holders

        if holders_df.empty:
            logger.warning(
                f"No institutional holders data found via yfinance for {ticker}"
            )
            return []

        holders_list = []
        for index, row in holders_df.head(limit).iterrows():
            # Format Date Reported
            date_rep_str = (
                str(row["Date Reported"].date())
                if isinstance(row.get("Date Reported"), pd.Timestamp)
                else str(row.get("Date Reported"))
            )

            # Format % Out
            percent_out_val = row.get("% Out")
            percent_out_str = (
                f"{percent_out_val * 100:.2f}%" if pd.notna(percent_out_val) else None
            )

            # Ensure shares is integer
            shares_val = int(row["Shares"]) if pd.notna(row.get("Shares")) else 0

            holders_list.append(
                InstitutionalHolder(
                    holder=str(row["Holder"]),
                    shares=shares_val,
                    date_reported=date_rep_str,
                    percentOut=percent_out_str,  # Alias handled by Pydantic
                    value=float(row["Value"]) if pd.notna(row.get("Value")) else None,
                ).model_dump(exclude_none=True, by_alias=True)
            )
        return holders_list
    except Exception as e:
        logger.exception(
            f"Error fetching direct institutional holders for {ticker}: {e}"
        )
        raise HTTPException(
            status_code=500,
            detail=f"Internal server error fetching institutional holders for {ticker}: {str(e)}",
        )


class TrendData(BaseModel):
    ticker: str
    current_price: Optional[float] = None
    sma_short: Optional[float] = Field(
        None, alias="sma_50_day"
    )  # Example alias if needed
    sma_long: Optional[float] = Field(None, alias="sma_200_day")
    trend_signal: Optional[str] = None


@app.get("/trend/{ticker}", response_model=TrendData, tags=["Direct Data - Analysis"])
async def get_trend_direct(
    ticker: str,
    window1: int = Query(50, description="Short-term SMA window", ge=5, le=100),
    window2: int = Query(200, description="Long-term SMA window", ge=50, le=300),
):
    # Use the function tool logic directly for calculation
    try:
        trend_result = functionTool.calculate_price_trend(
            ticker=ticker,
            data_vendor="yfinance",  # Or allow selection?
            window1=window1,
            window2=window2,
        )
        if "error" in trend_result:
            raise HTTPException(status_code=404, detail=trend_result["error"])

        # Map result to response model (adjust keys/aliases if needed)
        return TrendData(
            ticker=trend_result["ticker"],
            current_price=trend_result.get("current_price"),
            sma_short=trend_result.get(f"sma_{window1}_day"),
            sma_long=trend_result.get(f"sma_{window2}_day"),
            trend_signal=trend_result.get("trend_signal"),
        )
    except HTTPException as http_exc:
        raise http_exc
    except Exception as e:
        logger.exception(f"Error fetching direct trend data for {ticker}: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Internal server error fetching trend for {ticker}: {str(e)}",
        )


# Add similar direct endpoints for calculate_period_statistics and calculate_returns if desired
# Example for Statistics:
class StatisticsData(BaseModel):
    ticker: str
    start_date: str
    end_date: str
    mean_price: Optional[float] = None
    median_price: Optional[float] = None
    standard_deviation: Optional[float] = None
    volatility_percent: Optional[float] = None
    minimum_price: Optional[float] = None
    maximum_price: Optional[float] = None


@app.get(
    "/statistics/{ticker}",
    response_model=StatisticsData,
    tags=["Direct Data - Analysis"],
)
async def get_statistics_direct(
    ticker: str,
    start_date: Optional[str] = Query(
        None, description="Start date (YYYY-MM-DD), defaults to 1 year ago"
    ),
    end_date: Optional[str] = Query(
        None, description="End date (YYYY-MM-DD), defaults to today"
    ),
):
    try:
        stats_result = functionTool.calculate_period_statistics(
            ticker=ticker,
            data_vendor="yfinance",
            start_date=start_date,
            end_date=end_date,
        )
        if "error" in stats_result:
            raise HTTPException(status_code=404, detail=stats_result["error"])

        # Pydantic will automatically map matching keys
        return StatisticsData(**stats_result)

    except HTTPException as http_exc:
        raise http_exc
    except Exception as e:
        logger.exception(f"Error fetching direct statistics for {ticker}: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Internal server error fetching statistics for {ticker}: {str(e)}",
        )


# Example for Returns:
class ReturnsData(BaseModel):
    ticker: str
    start_date_used: str
    end_date_used: str
    start_price: Optional[float] = None
    end_price: Optional[float] = None
    total_return_percent: Optional[float] = None
    annualized_return_percent: Optional[float] = None


@app.get(
    "/returns/{ticker}", response_model=ReturnsData, tags=["Direct Data - Analysis"]
)
async def get_returns_direct(
    ticker: str,
    start_date: Optional[str] = Query(
        None, description="Start date (YYYY-MM-DD), defaults to 1 year ago"
    ),
    end_date: Optional[str] = Query(
        None, description="End date (YYYY-MM-DD), defaults to today"
    ),
):
    try:
        returns_result = functionTool.calculate_returns(
            ticker=ticker,
            data_vendor="yfinance",
            start_date=start_date,
            end_date=end_date,
        )
        if "error" in returns_result:
            raise HTTPException(status_code=404, detail=returns_result["error"])

        # Pydantic will automatically map matching keys
        return ReturnsData(**returns_result)

    except HTTPException as http_exc:
        raise http_exc
    except Exception as e:
        logger.exception(f"Error fetching direct returns for {ticker}: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Internal server error fetching returns for {ticker}: {str(e)}",
        )
