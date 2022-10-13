from typing import List
from unittest.mock import Mock

import inject
import pytest

from src.domain.category.category import Category
from src.domain.category.input.category_service import CategoryService
from src.domain.product.product import (
    Product, ProductCreateIn, ProductCreateOut, ProductUpdateIn, ProductUpdateOut
)
from src.domain.product.product_service_impl import ProductServiceImpl
from src.domain.product.output.product_repository import ProductRepository


@pytest.fixture
def product_repository() -> Mock:
    return Mock()


@pytest.fixture
def category_service() -> Mock:
    return Mock()


@pytest.fixture
def injector(product_repository: Mock, category_service: Mock) -> None:
    def config(binder: inject.Binder) -> None:
        binder.bind(ProductRepository, product_repository)
        binder.bind(CategoryService, category_service)

    inject.clear_and_configure(config)


@pytest.fixture
def category() -> Category:
    return Category(
        id=1,
        name="vegetables",
    )


@pytest.fixture
def product(category: Category) -> Product:
    return Product(
        id=1,
        name="tomate",
        stock=1,
        price=1,
        pvp=1,
        has_discount=True,
        category=category,
    )


@pytest.fixture
def product2(category: Category) -> Product:
    return Product(
        id=1,
        name="tomate",
        stock=1,
        price=1,
        pvp=1,
        has_discount=True,
        category=category,
    )


@pytest.fixture
def products(product: Product, product2: Product) -> List[Product]:
    return [
        product,
        product2,
    ]


@pytest.fixture
def product_create_in() -> ProductCreateIn:
    return ProductCreateIn(
        name="Potato",
        stock=1,
        price=1,
        pvp=1,
        has_discount=True,
        category_id=1,
    )


@pytest.fixture
def product_create_out() -> ProductCreateOut:
    return ProductCreateOut(
        id=1,
        name="Potato",
        stock=1,
        price=1,
        pvp=1,
        has_discount=True,
        category_id=1,
    )


@pytest.fixture
def product_update_in() -> ProductUpdateIn:
    return ProductUpdateIn(
        name="product1",
        stock=1,
        price=1,
        pvp=1,
        has_discount=True,
        category_id=1,
    )


@pytest.fixture
def product_update_out() -> ProductUpdateOut:
    return ProductUpdateOut(
        id=1,
        name="product1",
        stock=1,
        price=1,
        pvp=1,
        has_discount=True,
        category_id=1,
    )


class TestProductServiceImpl:
    def test_should_return_list_products(
            self, injector: None, product_repository: Mock, products: List[Product]) -> None:
        product_repository.list.return_value = products
        products_result = ProductServiceImpl().list()
        assert products_result == products
        first_product, _ = products_result
        assert isinstance(first_product, Product)
        product_repository.list.assert_called_once()

    def test_should_return_product_by_id(
            self, injector: None, product_repository: Mock, product: Product) -> None:
        product_repository.get.return_value = product
        product_result = ProductServiceImpl().get(1)
        assert product_result == product
        assert isinstance(product_result, Product)
        product_repository.get.assert_called_once_with(1)

    def test_should_create_product_and_return_product_create_out(
            self, injector: None, product_repository: Mock,
            product_create_in: ProductCreateIn, product_create_out: ProductCreateOut,
            category_service: Mock, category: Category) -> None:
        product_repository.create.return_value = product_create_out
        category_service.get.return_value = category

        product_created_result = ProductServiceImpl().create(product_create_in)

        category_service.get.assert_called_once_with(product_create_in.category_id)
        assert product_created_result == product_create_out
        assert isinstance(product_created_result, ProductCreateOut)
        product_repository.create.assert_called_once_with(product_create_in)

    def test_should_update_product_and_return_product_update_out(
            self, injector: None, product_repository: Mock,
            product_update_in: ProductUpdateIn, product_update_out: ProductUpdateOut) -> None:
        product_repository.update.return_value = product_update_out
        product_updated_result = ProductServiceImpl().update(1, product_update_in)
        assert product_updated_result == product_update_out
        assert isinstance(product_updated_result, ProductUpdateOut)
        product_repository.update.assert_called_once_with(1, product_update_in)

    def test_should_delete_product(
            self, injector: None, product_repository: Mock) -> None:
        ProductServiceImpl().delete(1)
        product_repository.delete.assert_called_once_with(1)
