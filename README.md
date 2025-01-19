# finchat mvp

TODO:
- [ ] Define base chat route
- [ ] complete financialdatasets.ai function tools
- [ ] logic to extract and use correct tool with parameters
- [ ] add more data vendors
- [ ] use pandasai for csv and mysql data
- [ ] rag on folders using hybrid search (keyword: BM25 and vector)

## Project Directory

```
.
├── app
│   ├── ai
│   │   ├── __init__.py
│   │   └── llm.py
│   ├── api
│   │   ├── chat.py
│   │   └── __init__.py
│   ├── constants
│   │   ├── __init__.py
│   │   ├── prompts.py
│   │   └── settings.py
│   ├── dataVendors
│   │   ├── baseDataVendor.py
│   │   ├── dataVendorFactory.py
│   │   ├── financialDatasetsAI
│   │   │   ├── __init__.py
│   │   │   └── vendor.py
│   │   ├── functionTool.py
│   │   ├── functionToolSchema.py
│   │   ├── __init__.py
│   │   └── yfinance
│   ├── __init__.py
│   └── main.py
├── data
├── Dockerfile
├── pyproject.toml
├── README.md
└── uv.lock
```

ai > llm.py : contains chat completion code with structured output and tools capability.
dataVendors > baseDataVendor.py : Data class to struture different vendors input and output
dataVendors > dataVendorFactory.py : Class to select vendor method
dataVendors > functionTool.py : function tools definition

## Setup

```bash
# Create and Activate Python Virtual Environment
python -m venv venv
source venv/bin/activate

# Install packages
pip install -e .

# Start Application
python app/main.py
```