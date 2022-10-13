from src.domain.category.category import Category, CategoryCreateOut, CategoryUpdateOut
from src.infrastructure.adapters.output.repositories.entities import CategoryEntity


class CategoryMapper:

    @staticmethod
    def entity_to_domain(category: CategoryEntity) -> Category:
        if not category:
            return category
        return Category(
            id=category.id,
            name=category.name
        )


class CategoryCreateOutMapper:
    @staticmethod
    def entity_to_domain(category: CategoryEntity) -> CategoryCreateOut:
        if not category:
            return category
        return CategoryCreateOut(
            id=category.id,
            name=category.name,
        )


class CategoryUpdateOutMapper:
    @staticmethod
    def entity_to_domain(category: CategoryEntity) -> CategoryUpdateOut:
        if not category:
            return category
        return CategoryUpdateOut(
            id=category.id,
            name=category.name
        )
