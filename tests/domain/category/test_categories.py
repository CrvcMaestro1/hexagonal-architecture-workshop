from typing import List
from unittest.mock import Mock

import inject
import pytest

from src.domain.category.category import (
    Category, CategoryCreateIn, CategoryCreateOut, CategoryUpdateIn, CategoryUpdateOut
)
from src.domain.category.category_service_impl import CategoryServiceImpl
from src.domain.category.output.category_repository import CategoryRepository


@pytest.fixture
def category_repository() -> Mock:
    return Mock()


@pytest.fixture
def injector(category_repository: Mock) -> None:
    def config(binder: inject.Binder) -> None:
        binder.bind(CategoryRepository, category_repository)

    inject.clear_and_configure(config)


@pytest.fixture
def category() -> Category:
    return Category(id=1, name="category")


@pytest.fixture
def categories() -> List[Category]:
    return [
        Category(id=1, name="category1"),
        Category(id=2, name="category2"),
    ]


@pytest.fixture
def category_create_in() -> CategoryCreateIn:
    return CategoryCreateIn(name="category")


@pytest.fixture
def category_create_out() -> CategoryCreateOut:
    return CategoryCreateOut(id=1, name="category")


@pytest.fixture
def category_update_in() -> CategoryUpdateIn:
    return CategoryUpdateIn(name="category1")


@pytest.fixture
def category_update_out() -> CategoryUpdateOut:
    return CategoryUpdateOut(id=1, name="category1")


class TestCategoryServiceImpl:
    def test_should_return_list_categories(
            self, injector: None, category_repository: Mock, categories: List[Category]) -> None:
        category_repository.list.return_value = categories
        categories_result = CategoryServiceImpl().list()
        assert categories_result == categories
        first_category, _ = categories_result
        assert isinstance(first_category, Category)
        category_repository.list.assert_called_once()

    def test_should_return_category_by_id(
            self, injector: None, category_repository: Mock, category: Category) -> None:
        category_repository.get.return_value = category
        category_result = CategoryServiceImpl().get(1)
        assert category_result == category
        assert isinstance(category_result, Category)
        category_repository.get.assert_called_once_with(1)

    def test_should_create_category_and_return_category_create_out(
            self, injector: None, category_repository: Mock,
            category_create_in: CategoryCreateIn, category_create_out: CategoryCreateOut) -> None:
        category_repository.create.return_value = category_create_out
        category_created_result = CategoryServiceImpl().create(category_create_in)
        assert category_created_result == category_create_out
        assert isinstance(category_created_result, CategoryCreateOut)
        category_repository.create.assert_called_once_with(category_create_in)

    def test_should_update_category_and_return_category_update_out(
            self, injector: None, category_repository: Mock,
            category_update_in: CategoryUpdateIn, category_update_out: CategoryUpdateOut) -> None:
        category_repository.update.return_value = category_update_out
        category_updated_result = CategoryServiceImpl().update(1, category_update_in)
        assert category_updated_result == category_update_out
        assert isinstance(category_updated_result, CategoryUpdateOut)
        category_repository.update.assert_called_once_with(1, category_update_in)

    def test_should_delete_category(
            self, injector: None, category_repository: Mock) -> None:
        CategoryServiceImpl().delete(1)
        category_repository.delete.assert_called_once_with(1)
