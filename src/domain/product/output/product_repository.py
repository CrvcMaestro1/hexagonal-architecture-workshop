from abc import (
    ABCMeta,
    abstractmethod
)
from typing import List

from src.domain.product.product import Product, ProductCreateOut, ProductCreateIn, ProductUpdateIn, ProductUpdateOut


class ProductRepository(metaclass=ABCMeta):

    @abstractmethod
    def list(self) -> List[Product]:
        pass

    @abstractmethod
    def get(self, product_id: int) -> Product:
        pass

    @abstractmethod
    def create(self, product: ProductCreateIn) -> ProductCreateOut:
        pass

    @abstractmethod
    def update(self, product_id: int, product: ProductUpdateIn) -> ProductUpdateOut:
        pass

    @abstractmethod
    def delete(self, product_id: int) -> None:
        pass
