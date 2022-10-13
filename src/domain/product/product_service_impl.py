from typing import List

import inject

from src.domain.category.input.category_service import CategoryService
from src.domain.product.input.product_service import ProductService
from src.domain.product.output.product_repository import ProductRepository
from src.domain.product.product import Product, ProductCreateOut, ProductUpdateOut, ProductCreateIn, ProductUpdateIn
from src.domain.utils.exceptions import ApplicationError


class ProductServiceImpl(ProductService):

    @inject.autoparams()
    def __init__(self, repository: ProductRepository, category_service: CategoryService):
        self.repository = repository
        self.category_service = category_service

    def list(self) -> List[Product]:
        return self.repository.list()

    def get(self, product_id: int) -> Product:
        product = self.repository.get(product_id)
        if not product:
            raise ApplicationError(404, 'Product does not found')
        return product

    def create(self, product: ProductCreateIn) -> ProductCreateOut:
        self.category_exists_or_raise_exception(product.category_id)
        return self.repository.create(product)

    def update(self, product_id: int, product: ProductUpdateIn) -> ProductUpdateOut:
        return self.repository.update(product_id, product)

    def delete(self, product_id: int) -> None:
        self.repository.delete(product_id)

    def category_exists_or_raise_exception(self, category_id: int) -> None:
        self.category_service.get(category_id)
