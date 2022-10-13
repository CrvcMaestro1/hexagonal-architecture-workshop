from datetime import date
from typing import Optional

import inject
from fastapi import APIRouter
from starlette import status

from src.domain.supplier_sales_history.input.supplier_sales_history_service import SupplierSalesHistoryService
from src.domain.supplier_sales_history.supplier_sales_history import SupplierSalesHistoryPaginator


@inject.autoparams()
def supplier_sales_history_router(supplier_sales_history_service: SupplierSalesHistoryService) -> APIRouter:
    router = APIRouter(tags=["supplier-statistics"])

    @router.get(
        '/supplier-sales-history', response_model=SupplierSalesHistoryPaginator,
        status_code=status.HTTP_200_OK
    )
    async def get_supplier_sales_history(
            billing_number: Optional[str] = None,
            payment_date_start: Optional[date] = None,
            payment_date_end: Optional[date] = None,
            payment_status: Optional[bool] = None,
            page: Optional[str] = None,
            page_size: Optional[str] = None
    ) -> SupplierSalesHistoryPaginator:
        supplier_sales_history = supplier_sales_history_service.get(billing_number, payment_date_start,
                                                                    payment_date_end, payment_status, page, page_size)

        return supplier_sales_history.to_dict()

    return router
