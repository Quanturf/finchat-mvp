from typing import Type, Optional

from .baseDataVendor import BaseDataVendor
from .financialDatasetsAI.vendor import FinancialDatasetsAI
from .yfinance.vendor import YahooFinance


class DataVendorFactory:
    """class to create all data vendors"""

    _vendors: dict[str, Type[BaseDataVendor]] = {
        "financialDatasetsAI": FinancialDatasetsAI,
        "yfinance": YahooFinance,
        # "alphaVantage": "AlphaVantage",
    }

    @classmethod
    def get_vendor(
        cls, vendor_name: str, api_key: Optional[str] = None
    ) -> BaseDataVendor:
        """
        Get vendor instance by name

        Args:
            vendor_name: Name of the vendor to use
            **kwargs: Additional arguments needed for vendor initialization
        """
        vendor_class = cls._vendors.get(vendor_name)
        if not vendor_class:
            raise ValueError(f"Unsupported vendor: {vendor_name}")

        return vendor_class(api_key=api_key)
