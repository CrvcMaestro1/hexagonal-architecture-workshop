from typing import Dict

from src.domain.supplier_sales_history.supplier_sales_history import (
    SupplierSalesHistoryPaginator, SupplierSalesHistoryValidator
)
from src.domain.utils.remote_mapper_validator import RemoteMapperValidator


class SupplierSalesHistoryPaginatorRemoteMapper(RemoteMapperValidator):
    required_keys = [
        ("results", list)
    ]

    def remote_to_domain(self, data: Dict, query_url: str) -> SupplierSalesHistoryPaginator:
        self.is_valid(data)
        results: list = data.get('results', list)
        optional_next = data.get('next')
        optional_previous = data.get('previous')
        supplier_sales_history_paginator = SupplierSalesHistoryPaginator(
            count=data.get('count')
        )
        next_value = supplier_sales_history_paginator.get_next(optional_next)
        supplier_sales_history_paginator.next = f"{query_url}{next_value}" if next_value else None

        previous_value = supplier_sales_history_paginator.get_previous(optional_previous)
        supplier_sales_history_paginator.previous = f"{query_url}{previous_value}" if previous_value else None

        validator = SupplierSalesHistoryValidator()
        supplier_sales_history_paginator.results = supplier_sales_history_paginator.get_results(results, validator)
        return supplier_sales_history_paginator
