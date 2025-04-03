from fastapi import FastAPI, HTTPException, Query
from typing import List, Optional, Dict
from pydantic import BaseModel, Field
from .api import chat
import yfinance as yf

app = FastAPI(
    title="QuantAI Finance Chatbot",
    version="0.1.0",
)

app.include_router(chat.chatRouter, prefix="/chat", tags=["chat"])


@app.get("/health")
async def health():
    return {"status": "ok"}


@app.get("/")
async def root():
    return {"message": "Welcome to the QuantAI Finance Chatbot!"}


class CompanyOfficer(BaseModel):
    maxAge: int
    name: str
    age: Optional[int] = None
    title: str
    yearBorn: Optional[int] = None
    fiscalYear: Optional[int] = None
    totalPay: Optional[int] = None
    exercisedValue: Optional[int] = None
    unexercisedValue: Optional[int] = None


class CompanyInfo(BaseModel):
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
    irWebsite: Optional[str] = None
    maxAge: Optional[int] = None

    # Pricing/Trading Info
    priceHint: Optional[int] = None
    previousClose: Optional[float] = None
    open: Optional[float] = None
    dayLow: Optional[float] = None
    dayHigh: Optional[float] = None
    regularMarketPreviousClose: Optional[float] = None
    regularMarketOpen: Optional[float] = None
    regularMarketDayLow: Optional[float] = None
    regularMarketDayHigh: Optional[float] = None
    payoutRatio: Optional[float] = None
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
    marketCap: Optional[int] = None
    fiftyTwoWeekLow: Optional[float] = None
    fiftyTwoWeekHigh: Optional[float] = None
    priceToSalesTrailing12Months: Optional[float] = None
    fiftyDayAverage: Optional[float] = None
    twoHundredDayAverage: Optional[float] = None
    trailingAnnualDividendRate: Optional[float] = None
    trailingAnnualDividendYield: Optional[float] = None
    currency: Optional[str] = None
    tradeable: Optional[bool] = None

    # Financials
    enterpriseValue: Optional[int] = None
    profitMargins: Optional[float] = None
    floatShares: Optional[int] = None
    sharesOutstanding: Optional[int] = None
    sharesShort: Optional[int] = None
    sharesShortPriorMonth: Optional[int] = None
    sharesShortPreviousMonthDate: Optional[int] = None
    dateShortInterest: Optional[int] = None
    sharesPercentSharesOut: Optional[float] = None
    heldPercentInsiders: Optional[float] = None
    heldPercentInstitutions: Optional[float] = None
    shortRatio: Optional[float] = None
    shortPercentOfFloat: Optional[float] = None
    impliedSharesOutstanding: Optional[int] = None
    bookValue: Optional[float] = None
    priceToBook: Optional[float] = None
    lastFiscalYearEnd: Optional[int] = None
    nextFiscalYearEnd: Optional[int] = None
    mostRecentQuarter: Optional[int] = None
    earningsQuarterlyGrowth: Optional[float] = None
    netIncomeToCommon: Optional[int] = None
    trailingEps: Optional[float] = None
    forwardEps: Optional[float] = None
    lastSplitFactor: Optional[str] = None
    lastSplitDate: Optional[int] = None
    enterpriseToRevenue: Optional[float] = None
    enterpriseToEbitda: Optional[float] = None
    fiftyTwoWeekChange: Optional[float] = None
    SandP52WeekChange: Optional[float] = Field(None, alias="SandP52WeekChange")
    quoteType: Optional[str] = None
    currentPrice: Optional[float] = None
    targetHighPrice: Optional[float] = None
    targetLowPrice: Optional[float] = None
    targetMeanPrice: Optional[float] = None
    targetMedianPrice: Optional[float] = None
    recommendationMean: Optional[float] = None
    recommendationKey: Optional[str] = None
    numberOfAnalystOpinions: Optional[int] = None
    totalCash: Optional[int] = None
    totalCashPerShare: Optional[float] = None
    ebitda: Optional[int] = None
    totalDebt: Optional[int] = None
    quickRatio: Optional[float] = None
    currentRatio: Optional[float] = None
    totalRevenue: Optional[int] = None
    debtToEquity: Optional[float] = None
    revenuePerShare: Optional[float] = None
    returnOnAssets: Optional[float] = None
    returnOnEquity: Optional[float] = None
    grossProfits: Optional[int] = None
    freeCashflow: Optional[int] = None
    operatingCashflow: Optional[int] = None
    earningsGrowth: Optional[float] = None
    revenueGrowth: Optional[float] = None
    grossMargins: Optional[float] = None
    ebitdaMargins: Optional[float] = None
    operatingMargins: Optional[float] = None
    financialCurrency: Optional[str] = None
    symbol: str = ""

    # Other Details
    language: Optional[str] = None
    region: Optional[str] = None
    typeDisp: Optional[str] = None
    quoteSourceName: Optional[str] = None
    triggerable: Optional[bool] = None
    customPriceAlertConfidence: Optional[str] = None
    hasPrePostMarketData: Optional[bool] = None
    firstTradeDateMilliseconds: Optional[int] = None
    earningsCallTimestampStart: Optional[int] = None
    earningsCallTimestampEnd: Optional[int] = None
    isEarningsDateEstimate: Optional[bool] = None
    epsTrailingTwelveMonths: Optional[float] = None
    epsForward: Optional[float] = None
    epsCurrentYear: Optional[float] = None
    priceEpsCurrentYear: Optional[float] = None
    fiftyDayAverageChange: Optional[float] = None
    fiftyDayAverageChangePercent: Optional[float] = None
    twoHundredDayAverageChange: Optional[float] = None
    corporateActions: List[Dict] = Field(default_factory=list)
    postMarketTime: Optional[int] = None
    regularMarketTime: Optional[int] = None
    exchange: Optional[str] = None
    messageBoardId: Optional[str] = None
    exchangeTimezoneName: Optional[str] = None
    exchangeTimezoneShortName: Optional[str] = None
    gmtOffSetMilliseconds: Optional[int] = None
    market: Optional[str] = None
    esgPopulated: Optional[bool] = None
    shortName: Optional[str] = None
    longName: Optional[str] = None
    regularMarketChangePercent: Optional[float] = None
    regularMarketPrice: Optional[float] = None
    marketState: Optional[str] = None
    twoHundredDayAverageChangePercent: Optional[float] = None
    sourceInterval: Optional[int] = None
    exchangeDataDelayedBy: Optional[int] = None
    averageAnalystRating: Optional[str] = None
    cryptoTradeable: Optional[bool] = None
    postMarketChangePercent: Optional[float] = None
    postMarketPrice: Optional[float] = None
    postMarketChange: Optional[float] = None
    regularMarketChange: Optional[float] = None
    regularMarketDayRange: Optional[str] = None
    fullExchangeName: Optional[str] = None
    averageDailyVolume3Month: Optional[int] = None
    fiftyTwoWeekLowChange: Optional[float] = None
    fiftyTwoWeekLowChangePercent: Optional[float] = None
    fiftyTwoWeekRange: Optional[str] = None
    fiftyTwoWeekHighChange: Optional[float] = None
    fiftyTwoWeekHighChangePercent: Optional[float] = None
    fiftyTwoWeekChangePercent: Optional[float] = None
    earningsTimestamp: Optional[int] = None
    earningsTimestampStart: Optional[int] = None
    earningsTimestampEnd: Optional[int] = None
    displayName: Optional[str] = None
    trailingPegRatio: Optional[float] = None


@app.get("/company_info/{ticker}", response_model=CompanyInfo)
async def get_company_info(ticker: str):
    try:
        company = yf.Ticker(ticker)
        info = company.info

        data = {}
        for key, value in info.items():
            data[key] = value

        company_officers = []
        for officer in data.get("companyOfficers", []):
            try:
                company_officers.append(CompanyOfficer(**officer).model_dump())
            except Exception as e:
                print(f"Error parsing officer data: {officer}, error: {e}")
                continue
        data["companyOfficers"] = company_officers
        return CompanyInfo(**data)

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


class Earnings(BaseModel):
    date: str
    epsActual: Optional[float] = None
    epsEstimate: Optional[float] = None
    epsDifference: Optional[float] = None
    surprisePercent: Optional[float] = None


@app.get("/earnings/{ticker}", response_model=List[Earnings])
async def get_earnings(
    ticker: str,
    last: int = Query(4, description="Number of last earnings quarters to retrieve"),
):
    try:
        company = yf.Ticker(ticker)
        earnings_history = company.earnings_history

        earnings_list = []
        for index, row in earnings_history.iterrows():
            earnings_list.append(
                Earnings(
                    date=str(index),
                    epsActual=row.get("epsActual"),
                    epsEstimate=row.get("epsEstimate"),
                    epsDifference=row.get("epsDifference"),
                    surprisePercent=row.get("surprisePercent"),
                )
            )
        return earnings_list
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


class FinancialStatementResponse(BaseModel):
    statement: Dict


@app.get("/financial_statements/{ticker}")
async def get_financial_statements(
    ticker: str,
    statement_type: str = Query(
        ...,
        description="Type of financial statement (income_statement, balance_sheet, cash_flow_statement)",
    ),
    period: str = Query("annual", description="Period (annual, quarterly)"),
):
    try:
        company = yf.Ticker(ticker)

        if statement_type == "income_statement":
            if period == "annual":
                statement = company.income_stmt.to_dict()
            elif period == "quarterly":
                statement = company.quarterly_income_stmt.to_dict()
            else:
                raise HTTPException(
                    status_code=400,
                    detail="Invalid period. Choose 'annual' or 'quarterly'.",
                )
        elif statement_type == "balance_sheet":
            if period == "annual":
                statement = company.balance_sheet.to_dict()
            elif period == "quarterly":
                statement = company.quarterly_balance_sheet.to_dict()
            else:
                raise HTTPException(
                    status_code=400,
                    detail="Invalid period. Choose 'annual' or 'quarterly'.",
                )
        elif statement_type == "cash_flow_statement":
            if period == "annual":
                statement = company.cashflow.to_dict()
            elif period == "quarterly":
                statement = company.quarterly_cashflow.to_dict()
            else:
                raise HTTPException(
                    status_code=400,
                    detail="Invalid period. Choose 'annual' or 'quarterly'.",
                )
        else:
            raise HTTPException(
                status_code=400,
                detail="Invalid statement_type. Choose 'income_statement', 'balance_sheet', or 'cash_flow_statement'.",
            )
        return FinancialStatementResponse(statement=statement)

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


class SECFiling(BaseModel):
    date: str
    form_type: str
    link: Optional[str]
    epochDate: Optional[int] = None
    title: Optional[str] = None


@app.get("/sec_filings/{ticker}", response_model=List[SECFiling])
async def get_sec_filings(
    ticker: str,
    filing_type: Optional[str] = Query(
        None, description="Type of SEC filing (e.g., 10-K, 10-Q, 8-K)"
    ),
    last: int = Query(5, description="number of last filings to be returned"),
):
    try:
        company = yf.Ticker(ticker)
        filings = company.get_sec_filings()
        
        filings_list = []
        for filing in filings:
            if filing_type and filing.get("type") != filing_type:
                continue

            filings_list.append(
                SECFiling(
                    date=str(filing.get("date")),
                    form_type=filing.get("type"),
                    link=filing.get("edgarUrl"),
                    epochDate=filing.get("epochDate"),
                    title=filing.get("title"),
                )
            )
            if len(filings_list) >= last:
                break

        return filings_list

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


class FinancialMetric(BaseModel):
    metric_name: str
    value: str


@app.get("/financial_metrics/{ticker}", response_model=List[FinancialMetric])
async def get_financial_metrics(ticker: str):
    try:
        company = yf.Ticker(ticker)
        info = company.info

        metrics = [
            {"metric_name": "Market Cap", "value": str(info.get("marketCap"))},
            {"metric_name": "PE Ratio (TTM)", "value": str(info.get("trailingPE"))},
            {"metric_name": "Forward PE", "value": str(info.get("forwardPE"))},
            {
                "metric_name": "Dividend Yield",
                "value": str(info.get("trailingAnnualDividendYield")),
            },
            {"metric_name": "Beta", "value": str(info.get("beta"))},
        ]
        return [FinancialMetric(**m) for m in metrics]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


class HistoricalPriceData(BaseModel):
    date: str
    open: float
    high: float
    low: float
    close: float
    volume: int


@app.get("/historical_prices/{ticker}", response_model=List[HistoricalPriceData])
async def get_historical_prices(
    ticker: str,
    start_date: str = Query(..., description="Start date (YYYY-MM-DD)"),
    end_date: str = Query(..., description="End date (YYYY-MM-DD)"),
    interval: str = Query("1d", description="Interval (1d, 1wk, 1mo)"),
):
    try:
        company = yf.Ticker(ticker)
        history = company.history(start=start_date, end=end_date, interval=interval)

        prices = []
        for index, row in history.iterrows():
            prices.append(
                HistoricalPriceData(
                    date=str(index.date()),
                    open=row["Open"],
                    high=row["High"],
                    low=row["Low"],
                    close=row["Close"],
                    volume=int(row["Volume"]),
                )
            )
        return prices
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


class NewsItem(BaseModel):
    title: str
    description: str
    summary: str
    publisher: str
    link: str
    publish_time: str


@app.get("/news/{ticker}", response_model=List[NewsItem])
async def get_news(
    ticker: str, last: int = Query(5, description="Number of articles to retrieve")
):
    try:
        company = yf.Ticker(ticker)
        news_list = []
        for item in company.news[:last]:
            news_list.append(
                NewsItem(
                    title=item["content"]["title"],
                    description=item["content"]["description"],
                    summary=item["content"]["summary"],
                    publisher=item["content"]["provider"]["displayName"],
                    link=item["content"]["canonicalUrl"]["url"],
                    publish_time=item["content"]["pubDate"],
                )
            )
        return news_list
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


class InstitutionalHolder(BaseModel):
    holder: str
    shares: int
    date_reported: str


@app.get("/institutional_holders/{ticker}", response_model=List[InstitutionalHolder])
async def get_institutional_holders(ticker: str):
    try:
        company = yf.Ticker(ticker)
        holders = company.institutional_holders
        holders_list = []
        for index, row in holders.iterrows():
            holders_list.append(
                InstitutionalHolder(
                    holder=row["Holder"],
                    shares=row["Shares"],
                    date_reported=str(row["Date Reported"]),
                )
            )
        return holders_list
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


class ChartData(BaseModel):
    labels: List[str]
    data: List[float]


@app.get("/chart/{ticker}")
async def get_chart(
    ticker: str,
    start_date: str = Query(..., description="Start date (YYYY-MM-DD)"),
    end_date: str = Query(..., description="End date (YYYY-MM-DD)"),
    chart_type: str = Query("line", description="Chart type (line, bar)"),
    interval: str = Query("1d", description="data interval"),
):
    try:
        company = yf.Ticker(ticker)
        history = company.history(start=start_date, end=end_date, interval=interval)

        if chart_type == "line":
            labels = [str(date.date()) for date in history.index]
            data = history["Close"].tolist()
        elif chart_type == "bar":
            labels = [str(date.date()) for date in history.index]
            data = history["Volume"].tolist()
        else:
            raise HTTPException(status_code=400, detail="Invalid chart_type")

        return ChartData(labels=labels, data=data)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/sma_comparison/{ticker}")
async def compare_sma(ticker: str):
    try:
        company = yf.Ticker(ticker)
        data = company.history(period="1y")
        data["SMA50"] = data["Close"].rolling(window=50).mean()
        data["SMA200"] = data["Close"].rolling(window=200).mean()
        current_price = data["Close"].iloc[-1]
        sma50 = data["SMA50"].iloc[-1]
        sma200 = data["SMA200"].iloc[-1]

        return {
            "ticker": ticker,
            "current_price": current_price,
            "sma50": sma50,
            "sma200": sma200,
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
