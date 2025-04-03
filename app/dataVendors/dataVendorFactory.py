from typing import Type, Optional
import logging

from .baseDataVendor import BaseDataVendor
from .financialDatasetsAI.vendor import FinancialDatasetsAI
from .yfinance.vendor import YahooFinance

logger = logging.getLogger(__name__)


class DataVendorFactory:
    _vendors: dict[str, Type[BaseDataVendor]] = {
        "financialDatasetsAI": FinancialDatasetsAI,
        "yfinance": YahooFinance,
    }

    @classmethod
    def get_vendor(
        cls, vendor_name: str, api_key: Optional[str] = None
    ) -> BaseDataVendor:
        vendor_class = cls._vendors.get(vendor_name.lower())
        if not vendor_class:
            logger.error(f"Unsupported vendor requested: {vendor_name}")
            raise ValueError(f"Unsupported vendor: {vendor_name}")

        try:
            logger.info(f"Creating instance of vendor: {vendor_name}")
            return vendor_class(api_key=api_key)
        except Exception as e:
            logger.error(f"Failed to instantiate vendor {vendor_name}: {e}")
            raise ValueError(f"Failed to initialize vendor {vendor_name}: {str(e)}")
