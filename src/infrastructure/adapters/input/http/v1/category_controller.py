from typing import List

import inject
from fastapi import APIRouter
from starlette import status

from src.domain.category.category import (
    Category, CategoryCreateOut, CategoryCreateIn, CategoryUpdateOut, CategoryUpdateIn
)
from src.domain.category.input.category_service import CategoryService


@inject.autoparams()
def category_router(
        category_service: CategoryService
) -> APIRouter:
    router = APIRouter(tags=["category"])

    @router.get('/categories', response_model=List[Category], status_code=status.HTTP_200_OK)
    async def category_list() -> List[Category]:
        categories = category_service.list()
        return [category.to_dict() for category in categories]

    @router.get('/categories/{category_id}', response_model=Category, status_code=status.HTTP_200_OK)
    async def get_category(category_id: int) -> Category:
        category = category_service.get(category_id)
        return category.to_dict()

    @router.post('/categories', response_model=CategoryCreateOut, status_code=status.HTTP_201_CREATED)
    async def category_create(category: CategoryCreateIn) -> CategoryCreateOut:
        category = category_service.create(category)
        return category.to_dict()

    @router.put('/categories/{category_id}', response_model=CategoryUpdateOut, status_code=status.HTTP_200_OK)
    async def category_update(category_id: int, category: CategoryUpdateIn) -> CategoryUpdateOut:
        category = category_service.update(category_id, category)
        return category.to_dict()

    @router.delete('/categories/{category_id}', status_code=status.HTTP_204_NO_CONTENT)
    async def category_delete(category_id: int) -> None:
        category_service.delete(category_id)

    return router
