from datetime import date
from typing import List, Dict, Any
from unittest.mock import Mock

import inject
import pytest

from src.domain.supplier_sales_history.output.supplier_sales_history_repository import SupplierSalesHistoryRepository
from src.domain.supplier_sales_history.supplier_sales_history import SupplierSalesHistory, SupplierSalesHistoryPaginator
from src.domain.supplier_sales_history.supplier_sales_history_service_impl import SupplierSalesHistoryServiceImpl
from src.domain.utils.exceptions import ApplicationError


@pytest.fixture
def supplier_sales_history_repository() -> Mock:
    return Mock()


@pytest.fixture
def injector(supplier_sales_history_repository: Mock) -> None:
    def config(binder: inject.Binder) -> None:
        binder.bind(SupplierSalesHistoryRepository, supplier_sales_history_repository)

    inject.clear_and_configure(config)


@pytest.fixture
def supplier_sales_history_paginator() -> SupplierSalesHistoryPaginator:
    return SupplierSalesHistoryPaginator(
        count=2,
        next="payment_date_start=2022-01-01&payment_date_end=2022-05-01&page=2&page_size=2",
        previous=None,
        results=[
            SupplierSalesHistory(
                sale_date=date(2022, 1, 2), document="001-101-000000389", subtotal=10, iva=1.2, total=11.20,
                withholding_tax=1.0, withholding_iva=1.20, payment_net=11.20, payment_status="PENDING"),
            SupplierSalesHistory(
                sale_date=date(2022, 1, 3), document="001-101-000000389", subtotal=10, iva=1.2, total=11.20,
                withholding_tax=1.0, withholding_iva=1.20, payment_net=11.20, payment_date=date(2022, 1, 2),
                payment_status="PENDING"),
        ]
    )


class TestSupplierSalesHistoryServiceImpl:

    def test_should_return_list_of_supplier_sales_history(
            self, injector: None, supplier_sales_history_repository: Mock,
            supplier_sales_history_paginator: SupplierSalesHistoryPaginator) -> None:
        supplier_sales_history_repository.get.return_value = supplier_sales_history_paginator
        supplier_id = 2
        payment_date_start = date(2022, 1, 1)
        payment_date_end = date(2022, 1, 10)
        page = 1
        page_str = str(page)
        page_size = 2
        page_size_str = str(page_size)

        supplier_sales_history_result = SupplierSalesHistoryServiceImpl().get(
            None, payment_date_start, payment_date_end, False, page_str, page_size_str
        )

        assert supplier_sales_history_result == supplier_sales_history_paginator
        supplier_sales_history_repository.get.assert_called_once_with(
            supplier_id, None, payment_date_start, payment_date_end, False, page_str, page_size_str
        )
        assert supplier_sales_history_repository.get.call_args.args[2] == payment_date_start
        assert supplier_sales_history_repository.get.call_args.args[3] == payment_date_end
        assert supplier_sales_history_repository.get.call_args.args[5] == page_str
        assert supplier_sales_history_repository.get.call_args.args[6] == page_size_str

    def test_should_return_application_error_when_there_are_no_sales(
            self, injector: None, supplier_sales_history_repository: Mock) -> None:
        supplier_sales_history_repository.get.return_value = None
        supplier_id = 2

        with pytest.raises(ApplicationError) as app_error:
            SupplierSalesHistoryServiceImpl().get()

        assert app_error.value.code == 404
        assert app_error.value.message == 'Supplier sales history does not found'
        supplier_sales_history_repository.get.assert_called_once_with(supplier_id, None, None, None, None, None, None)


@pytest.fixture
def supplier_sales_history() -> List[Dict[str, Any]]:
    return [
        {
            "date": "2022-03-29", "document": "001-101-000000547", "subtotal": 6425.54, "iva": 0.0,
            "total": 6425.54, "withholding_tax": 0.0, "withholding_iva": 0.0, "payment_net": 6425.54,
            "payment_date": None, "payment_status": "PENDING"
        },
        {
            "date": "2022-03-28", "document": "001-101-000000542", "subtotal": 20235.53, "iva": 2428.26,
            "total": 22663.79, "withholding_tax": 0.0, "withholding_iva": 0.0, "payment_net": 22663.79,
            "payment_date": None, "payment_status": "PENDING"
        }
    ]


class TestSupplierSalesHistoryPaginator:
    def test_should_return_empty_next_previous(self, supplier_sales_history: List[Dict[str, Any]]) -> None:
        supplier_sales_history_paginator = SupplierSalesHistoryPaginator(
            count=2
        )
        supplier_sales_history_paginator.next = supplier_sales_history_paginator.get_next()
        supplier_sales_history_paginator.previous = supplier_sales_history_paginator.get_previous()
        supplier_sales_history_paginator.results = supplier_sales_history_paginator.get_results(supplier_sales_history)

        assert len(supplier_sales_history_paginator.results) == 2
        assert supplier_sales_history_paginator.next is None
        assert supplier_sales_history_paginator.previous is None

    def test_should_return_next_and_empty_previous(self, supplier_sales_history: List[Dict[str, Any]]) -> None:
        supplier_sales_history_paginator = SupplierSalesHistoryPaginator(
            count=2
        )
        supplier_sales_history_paginator.next = supplier_sales_history_paginator.get_next(
            "http://testurl/?page=2&page_size=2")
        supplier_sales_history_paginator.previous = supplier_sales_history_paginator.get_previous()
        supplier_sales_history_paginator.results = supplier_sales_history_paginator.get_results(supplier_sales_history)

        assert len(supplier_sales_history_paginator.results) == 2
        assert supplier_sales_history_paginator.next == "page=2&page_size=2"
        assert supplier_sales_history_paginator.previous is None

    def test_should_return_previous_and_empty_next(self, supplier_sales_history: List[Dict[str, Any]]) -> None:
        supplier_sales_history_paginator = SupplierSalesHistoryPaginator(
            count=2
        )
        supplier_sales_history_paginator.next = supplier_sales_history_paginator.get_next()
        supplier_sales_history_paginator.previous = supplier_sales_history_paginator.get_previous(
            "http://testurl/?page=2&page_size=2")
        supplier_sales_history_paginator.results = supplier_sales_history_paginator.get_results(supplier_sales_history)

        assert len(supplier_sales_history_paginator.results) == 2
        assert supplier_sales_history_paginator.next is None
        assert supplier_sales_history_paginator.previous == "page=2&page_size=2"

    def test_should_return_previous_and_next(self, supplier_sales_history: List[Dict[str, Any]]) -> None:
        supplier_sales_history_paginator = SupplierSalesHistoryPaginator(
            count=2
        )
        supplier_sales_history_paginator.next = supplier_sales_history_paginator.get_next(
            "http://testurl/?page=3&page_size=2")
        supplier_sales_history_paginator.previous = supplier_sales_history_paginator.get_previous(
            "http://testurl/?page=1&page_size=2")
        supplier_sales_history_paginator.results = supplier_sales_history_paginator.get_results(supplier_sales_history)

        assert len(supplier_sales_history_paginator.results) == 2
        assert supplier_sales_history_paginator.next == "page=3&page_size=2"
        assert supplier_sales_history_paginator.previous == "page=1&page_size=2"
