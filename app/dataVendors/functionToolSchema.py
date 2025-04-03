GET_TICKER_PRICE_TOOL = {
    "type": "function",
    "function": {
        "name": "get_ticker_price",
        "description": "Get the latest closing price, change, and percent change for a given stock ticker. Use for current price status.",
        "parameters": {
            "type": "object",
            "properties": {
                "ticker": {
                    "type": "string",
                    "description": "The stock ticker symbol (e.g., AAPL, MSFT).",
                },
                "data_vendor": {
                    "type": "string",
                    "description": "The preferred data source",
                    "enum": ["yfinance", "financialDatasetsAI"],
                    "default": "yfinance",
                },
            },
            "required": ["ticker"],
        },
    },
}

GET_TICKER_HISTORY_TOOL = {
    "type": "function",
    "function": {
        "name": "get_ticker_history",
        "description": "Provides a summary of historical price data (start/end price, high, low, change, volume) for a stock ticker over a specified period. Use for summarizing performance over time. Defaults to last 1 month if dates omitted.",
        "parameters": {
            "type": "object",
            "properties": {
                "ticker": {
                    "type": "string",
                    "description": "The stock ticker symbol (e.g., AAPL, MSFT).",
                },
                "data_vendor": {
                    "type": "string",
                    "description": "The preferred data source",
                    "enum": ["yfinance", "financialDatasetsAI"],
                    "default": "yfinance",
                },
                "start_date": {
                    "type": "string",
                    "format": "date",
                    "description": "The start date for the historical data (YYYY-MM-DD). Optional, defaults to ~1 month ago.",
                },
                "end_date": {
                    "type": "string",
                    "format": "date",
                    "description": "The end date for the historical data (YYYY-MM-DD). Optional, defaults to today.",
                },
                "interval": {
                    "type": "string",
                    "description": "Data interval for summary calculation.",
                    "enum": ["day", "week", "month"],
                    "default": "day",
                },
            },
            "required": ["ticker"],
        },
    },
}

GET_COMPANY_INFO_TOOL = {
    "type": "function",
    "function": {
        "name": "get_company_info",
        "description": "Provides key information about a company (name, sector, industry, summary, market cap, P/E ratios, dividend yield, beta, etc.). Use for general company overview questions.",
        "parameters": {
            "type": "object",
            "properties": {
                "ticker": {
                    "type": "string",
                    "description": "The stock ticker symbol of the company (e.g., AAPL, MSFT).",
                },
                "data_vendor": {
                    "type": "string",
                    "description": "The preferred data source",
                    "enum": ["yfinance", "financialDatasetsAI"],
                    "default": "yfinance",
                },
            },
            "required": ["ticker"],
        },
    },
}

GET_INSTITUTIONAL_INVESTORS_TOOL = {
    "type": "function",
    "function": {
        "name": "get_institutional_investors",
        "description": "Provides a list of the top institutional investors (default 5) in a company by shares held. Use for questions about major shareholders.",
        "parameters": {
            "type": "object",
            "properties": {
                "ticker": {
                    "type": "string",
                    "description": "The stock ticker symbol of the company (e.g., AAPL, MSFT).",
                },
                "data_vendor": {
                    "type": "string",
                    "description": "The preferred data source",
                    "enum": ["yfinance", "financialDatasetsAI"],
                    "default": "yfinance",
                },
                "limit": {
                    "type": "integer",
                    "description": "Maximum number of top investors to return.",
                    "default": 5,
                },
            },
            "required": ["ticker"],
        },
    },
}

GET_SEC_FILINGS_TOOL = {
    "type": "function",
    "function": {
        "name": "get_sec_filings",
        "description": "Retrieves a list of recent SEC filings (like 10-K, 10-Q, 8-K) for a company, with links. Use for questions about official company reports and filings.",
        "parameters": {
            "type": "object",
            "properties": {
                "ticker": {
                    "type": "string",
                    "description": "The stock ticker symbol of the company (e.g., AAPL, MSFT).",
                },
                "data_vendor": {
                    "type": "string",
                    "description": "The preferred data source",
                    "enum": ["yfinance", "financialDatasetsAI"],
                    "default": "yfinance",
                },
                "filing_type": {
                    "type": "string",
                    "description": "Optional: Filter by specific SEC filing type (e.g., 10-K, 10-Q, 8-K). Ensure exact format.",
                    "enum": ["10-K", "10-Q", "8-K", "4", "13F", "S-1", "DEF 14A"],
                },
                "limit": {
                    "type": "integer",
                    "description": "Maximum number of filings to return.",
                    "default": 5,
                },
            },
            "required": ["ticker"],
        },
    },
}

GET_FINANCIAL_STATEMENTS_TOOL = {
    "type": "function",
    "function": {
        "name": "get_financial_statements",
        "description": "Retrieves a summary of key metrics from the latest 2 periods of a specific financial statement (income_statement, balance_sheet, cash_flow_statement) for a company. Use for questions about specific financial data like revenue, profit, assets, debt, or cash flow.",
        "parameters": {
            "type": "object",
            "properties": {
                "ticker": {
                    "type": "string",
                    "description": "The stock ticker symbol of the company (e.g., AAPL, MSFT).",
                },
                "data_vendor": {
                    "type": "string",
                    "description": "The preferred data source",
                    "enum": ["yfinance", "financialDatasetsAI"],
                    "default": "yfinance",
                },
                "statement_type": {
                    "type": "string",
                    "description": "The type of financial statement.",
                    "enum": [
                        "income_statement",
                        "balance_sheet",
                        "cash_flow_statement",
                    ],
                },
                "period": {
                    "type": "string",
                    "description": "The reporting period.",
                    "enum": ["annual", "quarterly"],
                    "default": "annual",
                },
            },
            "required": ["ticker", "statement_type"],
        },
    },
}

GET_FINANCIAL_NEWS_TOOL = {
    "type": "function",
    "function": {
        "name": "get_financial_news",
        "description": "Retrieves recent financial news headlines related to a company. Use for questions about latest news or events affecting a stock.",
        "parameters": {
            "type": "object",
            "properties": {
                "ticker": {
                    "type": "string",
                    "description": "The stock ticker symbol of the company (e.g., AAPL, MSFT).",
                },
                "data_vendor": {
                    "type": "string",
                    "description": "The preferred data source",
                    "enum": ["yfinance", "financialDatasetsAI"],
                    "default": "yfinance",
                },
                "limit": {
                    "type": "integer",
                    "description": "Maximum number of news items to return.",
                    "default": 3,
                },
            },
            "required": ["ticker"],
        },
    },
}

CALCULATE_PRICE_TREND_TOOL = {
    "type": "function",
    "function": {
        "name": "calculate_price_trend",
        "description": "Calculates the short-term (default 50-day) and long-term (default 200-day) simple moving averages (SMAs) and compares them to the current price to determine the current trend signal (e.g., Uptrend, Downtrend). Use for questions about the stock's current trend.",
        "parameters": {
            "type": "object",
            "properties": {
                "ticker": {
                    "type": "string",
                    "description": "The stock ticker symbol (e.g., AAPL, MSFT).",
                },
                "data_vendor": {
                    "type": "string",
                    "description": "The preferred data source",
                    "enum": ["yfinance", "financialDatasetsAI"],
                    "default": "yfinance",
                },
                "window1": {
                    "type": "integer",
                    "description": "Short-term moving average window.",
                    "default": 50,
                },
                "window2": {
                    "type": "integer",
                    "description": "Long-term moving average window.",
                    "default": 200,
                },
            },
            "required": ["ticker"],
        },
    },
}

CALCULATE_PERIOD_STATISTICS_TOOL = {
    "type": "function",
    "function": {
        "name": "calculate_period_statistics",
        "description": "Calculates key statistical measures (mean price, median price, standard deviation, volatility percentage, min/max price) for a stock over a specified period. Defaults to the last year if no dates provided. Use for understanding price behavior and volatility.",
        "parameters": {
            "type": "object",
            "properties": {
                "ticker": {
                    "type": "string",
                    "description": "The stock ticker symbol (e.g., AAPL, MSFT).",
                },
                "data_vendor": {
                    "type": "string",
                    "description": "The preferred data source",
                    "enum": ["yfinance", "financialDatasetsAI"],
                    "default": "yfinance",
                },
                "start_date": {
                    "type": "string",
                    "format": "date",
                    "description": "The start date for the statistical calculation (YYYY-MM-DD). Optional, defaults to 1 year ago.",
                },
                "end_date": {
                    "type": "string",
                    "format": "date",
                    "description": "The end date for the statistical calculation (YYYY-MM-DD). Optional, defaults to today.",
                },
            },
            "required": ["ticker"],
        },
    },
}


CALCULATE_RETURNS_TOOL = {
    "type": "function",
    "function": {
        "name": "calculate_returns",
        "description": "Calculates the total percentage return and annualized percentage return for a stock between a specified start and end date. Defaults to the last year if no dates provided. Use for quantifying investment performance over a period.",
        "parameters": {
            "type": "object",
            "properties": {
                "ticker": {
                    "type": "string",
                    "description": "The stock ticker symbol (e.g., AAPL, MSFT).",
                },
                "data_vendor": {
                    "type": "string",
                    "description": "The preferred data source",
                    "enum": ["yfinance", "financialDatasetsAI"],
                    "default": "yfinance",
                },
                "start_date": {
                    "type": "string",
                    "format": "date",
                    "description": "The start date for the return calculation (YYYY-MM-DD). Optional, defaults to 1 year ago.",
                },
                "end_date": {
                    "type": "string",
                    "format": "date",
                    "description": "The end date for the return calculation (YYYY-MM-DD). Optional, defaults to today.",
                },
            },
            "required": ["ticker"],
        },
    },
}


AVAILABLE_TOOLS = [
    GET_TICKER_PRICE_TOOL,
    GET_TICKER_HISTORY_TOOL,
    GET_COMPANY_INFO_TOOL,
    GET_INSTITUTIONAL_INVESTORS_TOOL,
    GET_SEC_FILINGS_TOOL,
    GET_FINANCIAL_STATEMENTS_TOOL,
    GET_FINANCIAL_NEWS_TOOL,
    CALCULATE_PRICE_TREND_TOOL,
    CALCULATE_PERIOD_STATISTICS_TOOL,
    CALCULATE_RETURNS_TOOL,
]
