from datetime import date
from typing import Optional

import inject

from src.domain.supplier_sales_history.input.supplier_sales_history_service import SupplierSalesHistoryService
from src.domain.supplier_sales_history.output.supplier_sales_history_repository import SupplierSalesHistoryRepository
from src.domain.supplier_sales_history.supplier_sales_history import SupplierSalesHistoryPaginator
from src.domain.utils.exceptions import ApplicationError


class SupplierSalesHistoryServiceImpl(SupplierSalesHistoryService):

    @inject.autoparams()
    def __init__(self, repository: SupplierSalesHistoryRepository):
        self.repository = repository

    def get(self,
            billing_number: Optional[str] = None,
            payment_date_start: Optional[date] = None,
            payment_date_end: Optional[date] = None,
            payment_status: Optional[bool] = None,
            page: Optional[str] = None,
            page_size: Optional[str] = None
            ) -> SupplierSalesHistoryPaginator:
        supplier_id: Optional[str] = '2'
        if not supplier_id:
            raise ApplicationError(400, 'Supplier ID does not provided')

        result = self.repository.get(
            int(supplier_id), billing_number, payment_date_start, payment_date_end, payment_status, page, page_size
        )

        if not result:
            raise ApplicationError(404, 'Supplier sales history does not found')

        return result
