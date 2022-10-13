from datetime import date
from typing import Optional

from src.domain.supplier_sales_history.output.supplier_sales_history_repository import SupplierSalesHistoryRepository
from src.domain.supplier_sales_history.supplier_sales_history import SupplierSalesHistoryPaginator
from src.domain.utils.exceptions import ApplicationError
from src.infrastructure.adapters.output.components.http import HttpConsumer, HttpMethod
from src.infrastructure.adapters.output.remote import MONOLITH_BASE_URL
from src.infrastructure.adapters.output.remote.mapper.supplier_sales_history_remote_mapper import (
    SupplierSalesHistoryPaginatorRemoteMapper
)


class SupplierSalesHistoryRepositoryRemoteImpl(SupplierSalesHistoryRepository):

    def get(self,
            supplier_id: int,
            billing_number: Optional[str] = None,
            payment_date_start: Optional[date] = None,
            payment_date_end: Optional[date] = None,
            payment_status: Optional[bool] = None, page: Optional[str] = None, page_size: Optional[str] = None,
            ) -> SupplierSalesHistoryPaginator:

        url = self.build_url(supplier_id, billing_number, payment_date_start, payment_date_end, payment_status, page,
                             page_size)

        response = HttpConsumer.consume(HttpMethod.GET, url)

        if not response.is_success:
            raise ApplicationError(
                response.status_code,
                'An error occurred while obtaining the supplier sales history.',
                response.data
            )
        data = response.data
        query_url = self.build_query_params(billing_number, payment_date_start, payment_date_end, payment_status)
        return SupplierSalesHistoryPaginatorRemoteMapper().remote_to_domain(data, query_url)

    @staticmethod
    def build_url(supplier_id: int,
                  billing_number: Optional[str] = None,
                  payment_date_start: Optional[date] = None,
                  payment_date_end: Optional[date] = None,
                  payment_status: Optional[bool] = None, page: Optional[str] = None,
                  page_size: Optional[str] = None) -> str:
        url = "{}/misuper/v2/invoices/{}/buy/history?".format(MONOLITH_BASE_URL, supplier_id)
        if payment_date_start and payment_date_end:
            url += f"start_date={payment_date_start}&end_date={payment_date_end}&"
        if billing_number:
            url += f"number={billing_number}&"
        if isinstance(payment_status, bool):
            url += f"invoice_paid={payment_status}&"
        if page:
            url += f"page={page}&"
        if page_size:
            url += f"page_size={page_size}"
        url = url.strip("&")
        return url

    @staticmethod
    def build_query_params(billing_number: Optional[str] = None,
                           payment_date_start: Optional[date] = None,
                           payment_date_end: Optional[date] = None,
                           payment_status: Optional[bool] = False) -> str:
        query_url = ""
        if billing_number:
            query_url += f"billing_number={billing_number}&"
        if payment_date_start:
            query_url += f"payment_date_start={payment_date_start}&"
        if payment_date_end:
            query_url += f"payment_date_end={payment_date_end}&"
        if payment_status:
            query_url += f"payment_status={payment_status}&"
        return query_url
