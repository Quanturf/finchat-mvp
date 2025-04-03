GET_TICKER_PRICE_TOOL = {
    "type": "function",
    "function": {
        "name": "get_ticker_price",
        "description": "Get the latest price for a given stock ticker. Use this tool when the user asks for the current or most recent price of a stock.",
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
                    "enum": ["yfinance"],
                },
            },
            "required": ["ticker", "data_vendor"],
        },
        "examples": [
            {"role": "user", "content": "What is the current price of TSLA?"},
            {"role": "user", "content": "Get the latest price for MSFT using yfinance"},
        ],
    },
}

GET_TICKER_HISTORY_TOOL = {
    "type": "function",
    "function": {
        "name": "get_ticker_history",
        "description": "Get the historical price data for a given stock ticker. Use this tool when the user asks for past prices or wants to see a chart of the stock's performance over a period of time.",
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
                    "enum": ["yfinance"],
                },
                "start_date": {
                    "type": "string",
                    "format": "date",
                    "description": "The start date for the historical data (YYYY-MM-DD).",
                },
                "end_date": {
                    "type": "string",
                    "format": "date",
                    "description": "The end date for the historical data (YYYY-MM-DD).",
                },
                "interval": {
                    "type": "string",
                    "description": "interval to get price for. Default must be '1wk'",
                    "enum": ["60m", "90m", "1h", "1d", "5d", "1wk", "1mo", "3mo"],
                },
            },
            "required": ["ticker", "data_vendor", "start_date", "end_date"],
        },
        "examples": [
            {"role": "user", "content": "What was the price of AAPL on 2023-01-15?"},
            {
                "role": "user",
                "content": "Show me the price history of GOOG from 2023-06-01 to 2023-12-31 using yfinance.",
            },
        ],
    },
}

GET_COMPANY_INFO_TOOL = {
    "type": "function",
    "function": {
        "name": "get_company_info",
        "description": "Provides general information about a company, such as its description, industry, sector, etc. Use this tool when the user asks questions like 'Tell me about Apple' or 'What does Microsoft do?'",
        "parameters": {
            "type": "object",
            "properties": {
                "ticker": {
                    "type": "string",
                    "description": "The stock ticker symbol of the company (e.g., AAPL, MSFT).",
                }
            },
            "required": ["ticker"],
        },
        "examples": [
            {"role": "user", "content": "Tell me about Tesla (TSLA)."},
            {"role": "user", "content": "What does NVDA do?"},
        ],
    },
}

GET_INSTITUTIONAL_INVESTORS_TOOL = {
    "type": "function",
    "function": {
        "name": "get_institutional_investors",
        "description": "Provides a list of the top institutional investors in a company. Use this tool when the user asks questions like 'Who are the major investors in Apple?' or 'Which institutions hold the most shares of Microsoft?'",
        "parameters": {
            "type": "object",
            "properties": {
                "ticker": {
                    "type": "string",
                    "description": "The stock ticker symbol of the company (e.g., AAPL, MSFT).",
                }
            },
            "required": ["ticker"],
        },
        "examples": [
            {"role": "user", "content": "Who are the major investors in TSLA?"},
            {
                "role": "user",
                "content": "Which institutions hold the most shares of AAPL?",
            },
        ],
    },
}

GET_SEC_FILINGS_TOOL = {
    "type": "function",
    "function": {
        "name": "get_sec_filings",
        "description": "Retrieves a list of recent SEC filings for a company. Use this tool when the user asks questions like 'What are the latest SEC filings for Apple?' or 'Show me the 10-K report for Microsoft.'",
        "parameters": {
            "type": "object",
            "properties": {
                "ticker": {
                    "type": "string",
                    "description": "The stock ticker symbol of the company (e.g., AAPL, MSFT).",
                },
                "filing_type": {
                    "type": "string",
                    "description": "The type of SEC filing (e.g., 10-K, 10-Q, 8-K).",
                },
            },
            "required": ["ticker"],
        },
        "examples": [
            {"role": "user", "content": "What are the latest SEC filings for TSLA?"},
            {"role": "user", "content": "Show me the 10-K report for MSFT."},
        ],
    },
}

GET_FINANCIAL_STATEMENTS_TOOL = {
    "type": "function",
    "function": {
        "name": "get_financial_statements",
        "description": "Retrieves financial statements (income statement, balance sheet, cash flow statement) for a company. Use this tool when the user asks questions like 'What is Apple's revenue?' or 'Show me Microsoft's balance sheet.'",
        "parameters": {
            "type": "object",
            "properties": {
                "ticker": {
                    "type": "string",
                    "description": "The stock ticker symbol of the company (e.g., AAPL, MSFT).",
                },
                "statement_type": {
                    "type": "string",
                    "description": "The type of financial statement (e.g., income_statement, balance_sheet, cash_flow_statement).",
                },
                "period": {
                    "type": "string",
                    "description": "The reporting period (e.g., annual, quarterly).",
                },
            },
            "required": ["ticker", "statement_type"],
        },
        "examples": [
            {"role": "user", "content": "What is AAPL's revenue?"},
            {"role": "user", "content": "Show me MSFT's balance sheet."},
        ],
    },
}

GET_FINANCIAL_NEWS_TOOL = {
    "type": "function",
    "function": {
        "name": "get_financial_news",
        "description": "Retrieves recent financial news articles related to a company. Use this tool when the user asks questions like 'What's the latest news on Apple?' or 'Any recent news about Microsoft?'",
        "parameters": {
            "type": "object",
            "properties": {
                "ticker": {
                    "type": "string",
                    "description": "The stock ticker symbol of the company (e.g., AAPL, MSFT).",
                }
            },
            "required": ["ticker"],
        },
        "examples": [
            {"role": "user", "content": "What's the latest news on TSLA?"},
            {"role": "user", "content": "Any recent news about MSFT?"},
        ],
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
]
