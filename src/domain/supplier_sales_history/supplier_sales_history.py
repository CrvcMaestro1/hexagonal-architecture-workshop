from datetime import date
from typing import Optional, List

from dataclasses_json import dataclass_json, LetterCase
from pydantic import BaseModel

from src.domain.utils.paginator import Paginator
from src.domain.utils.remote_mapper_validator import RemoteMapperValidator


@dataclass_json(letter_case=LetterCase.SNAKE)
class SupplierSalesHistoryBase(BaseModel):
    pass


@dataclass_json(letter_case=LetterCase.SNAKE)
class SupplierSalesHistory(SupplierSalesHistoryBase):
    sale_date: date
    document: Optional[str]
    subtotal: float
    iva: float
    total: float
    withholding_tax: float
    withholding_iva: float
    payment_net: float
    payment_date: Optional[date]
    payment_status: str


class SupplierSalesHistoryValidator(RemoteMapperValidator):
    required_keys = [
        ("date", date),
        ("sub_total", float),
        ("tax_total", float),
        ("total", float),
        ("retained_value", float),
        ("retained_iva_value", float),
        ("total", float),
        ("payment_status", str),
    ]


@dataclass_json(letter_case=LetterCase.SNAKE)
class SupplierSalesHistoryPaginator(SupplierSalesHistoryBase, Paginator):
    results: Optional[List[SupplierSalesHistory]]

    def get_results(
            self, results: List, validator: Optional[RemoteMapperValidator] = None
    ) -> List[SupplierSalesHistory]:
        supplier_payments_list: list[SupplierSalesHistory] = []
        if validator:
            validator.is_valid(results)
        for result in results:
            supplier_payments_list.append(SupplierSalesHistory(
                sale_date=result.get("date"),
                document=result.get("invoice_number"),
                subtotal=float(result.get("sub_total", float())),
                iva=float(result.get("tax_total", float())),
                total=float(result.get("total", float())),
                withholding_tax=float(result.get("retained_value", float())),
                withholding_iva=float(result.get("retained_iva_value", float())),
                payment_net=float(result.get("total", float())),
                payment_date=result.get("payment_date"),
                payment_status=result.get("payment_status")
            ))
        return supplier_payments_list

    def get_next(self, optional_next: Optional[str] = None) -> Optional[str]:
        return self.get_pagination(optional_next)

    def get_previous(self, optional_previous: Optional[str] = None) -> Optional[str]:
        return self.get_pagination(optional_previous)
