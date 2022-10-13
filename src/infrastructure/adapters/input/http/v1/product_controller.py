from typing import List

import inject
from fastapi import APIRouter
from starlette import status

from src.domain.product.input.product_service import ProductService
from src.domain.product.product import (
    Product, ProductCreateIn, ProductCreateOut, ProductUpdateIn, ProductUpdateOut
)


@inject.autoparams()
def product_router(
        product_service: ProductService
) -> APIRouter:
    router = APIRouter(tags=["product"])

    @router.get('/products', response_model=List[Product], status_code=status.HTTP_200_OK)
    async def product_list() -> List[Product]:
        products = product_service.list()
        return [product.to_dict() for product in products]

    @router.get('/products/{product_id}', response_model=Product, status_code=status.HTTP_200_OK)
    async def get_product(product_id: int) -> Product:
        product = product_service.get(product_id)
        return product.to_dict()

    @router.post('/products', response_model=ProductCreateOut, status_code=status.HTTP_201_CREATED)
    async def product_create(product: ProductCreateIn) -> ProductCreateOut:
        product = product_service.create(product)
        return product.to_dict()

    @router.put('/products/{product_id}', response_model=ProductUpdateOut, status_code=status.HTTP_200_OK)
    async def product_update(product_id: int, product: ProductUpdateIn) -> ProductUpdateOut:
        product = product_service.update(product_id, product)
        return product.to_dict()

    @router.delete('/products/{product_id}', status_code=status.HTTP_204_NO_CONTENT)
    async def product_delete(product_id: int) -> None:
        product_service.delete(product_id)

    return router
