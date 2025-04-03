from abc import ABC, abstractmethod
from typing import Optional, List, Dict
import pandas as pd


class BaseDataVendor(ABC):

    @abstractmethod
    def get_prices(
        self,
        ticker: str,
        interval: str = "day",
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        period: Optional[str] = None,
    ) -> pd.DataFrame:
        pass

    @abstractmethod
    def get_financial_statements(
        self, ticker: str, statement_type: str, period: str
    ) -> pd.DataFrame:
        pass

    @abstractmethod
    def get_company_info(self, ticker: str) -> Optional[pd.Series]:
        pass

    @abstractmethod
    def get_institutional_holders(self, ticker: str) -> pd.DataFrame:
        pass

    @abstractmethod
    def get_sec_filings(self, ticker: str) -> List[Dict]:
        pass

    @abstractmethod
    def get_news(self, ticker: str) -> List[Dict]:
        pass
