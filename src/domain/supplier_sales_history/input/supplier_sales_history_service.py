from abc import (
    ABCMeta,
    abstractmethod
)
from datetime import date
from typing import Optional

from src.domain.supplier_sales_history.supplier_sales_history import SupplierSalesHistoryPaginator


class SupplierSalesHistoryService:
    __metaclass__ = ABCMeta

    @abstractmethod
    def get(self,
            billing_number: Optional[str] = None,
            payment_date_start: Optional[date] = None,
            payment_date_end: Optional[date] = None,
            payment_status: Optional[bool] = None,
            page: Optional[str] = None,
            page_size: Optional[str] = None
            ) -> SupplierSalesHistoryPaginator:
        pass
