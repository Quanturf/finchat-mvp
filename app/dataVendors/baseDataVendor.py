from abc import ABC, abstractmethod
from typing import Optional
import pandas as pd


class BaseDataVendor(ABC):
    """Abstract class for all data vendors"""

    @abstractmethod
    def get_prices(
        self,
        ticker: str,
        interval: str = "day",
        interval_multiplier: int = 1,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
    ) -> pd.DataFrame:
        """Get ticker price data"""
        pass

    @abstractmethod
    def get_financial_statements(self):
        """Get financial statements"""
        pass

    @abstractmethod
    def get_company_info(self):
        """Get company information"""
        pass
