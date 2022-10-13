from abc import (
    ABCMeta,
    abstractmethod
)
from typing import List

from src.domain.category.category import (
    Category, CategoryCreateIn, CategoryCreateOut, CategoryUpdateIn, CategoryUpdateOut
)


class CategoryService:
    __metaclass__ = ABCMeta

    @abstractmethod
    def list(self) -> List[Category]:
        pass

    @abstractmethod
    def get(self, category_id: int) -> Category:
        pass

    @abstractmethod
    def create(self, category: CategoryCreateIn) -> CategoryCreateOut:
        pass

    @abstractmethod
    def update(self, category_id: int, category: CategoryUpdateIn) -> CategoryUpdateOut:
        pass

    @abstractmethod
    def delete(self, category_id: int) -> None:
        pass
