from typing import List

import inject

from src.domain.category.category import (
    Category, CategoryCreateIn, CategoryCreateOut, CategoryUpdateIn, CategoryUpdateOut
)
from src.domain.category.input.category_service import CategoryService
from src.domain.category.output.category_repository import CategoryRepository
from src.domain.utils.exceptions import ApplicationError


class CategoryServiceImpl(CategoryService):

    @inject.autoparams()
    def __init__(self, repository: CategoryRepository):
        self.repository = repository

    def list(self) -> List[Category]:
        return self.repository.list()

    def get(self, category_id: int) -> Category:
        category = self.repository.get(category_id)
        if not category:
            raise ApplicationError(404, 'Category does not found')
        return category

    def create(self, category: CategoryCreateIn) -> CategoryCreateOut:
        return self.repository.create(category)

    def update(self, category_id: int, category: CategoryUpdateIn) -> CategoryUpdateOut:
        return self.repository.update(category_id, category)

    def delete(self, category_id: int) -> None:
        self.repository.delete(category_id)
