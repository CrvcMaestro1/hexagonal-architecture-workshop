import os
from typing import List, Any

import inject
from fastapi import FastAPI
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from starlette import status
from starlette.responses import JSONResponse

from src.domain.product.input.product_service import ProductService
from src.domain.product.output.product_repository import ProductRepository
from src.domain.product.product_service_impl import ProductServiceImpl
from src.domain.room.default_room_service import DefaultRoomService
from src.domain.room.input.room_service import RoomService
from src.domain.room.output.room_repository import RoomRepository

from src.domain.supplier_sales_history.input.supplier_sales_history_service import SupplierSalesHistoryService
from src.domain.supplier_sales_history.output.supplier_sales_history_repository import SupplierSalesHistoryRepository
from src.domain.supplier_sales_history.supplier_sales_history_service_impl import SupplierSalesHistoryServiceImpl
from src.infrastructure.adapters.output.remote.supplier_sales_history_repository_remote_impl import (
    SupplierSalesHistoryRepositoryRemoteImpl
)
from src.infrastructure.adapters.output.repositories.default_room_repository import DefaultRoomRepository
from src.infrastructure.adapters.output.repositories.product_repository_impl import ProductRepositoryImpl


def configure_inject() -> None:
    def config(binder: inject.Binder) -> None:
        binder.bind_to_provider(RoomRepository, DefaultRoomRepository)
        binder.bind_to_provider(ProductRepository, ProductRepositoryImpl)

        binder.bind_to_provider(SupplierSalesHistoryRepository, SupplierSalesHistoryRepositoryRemoteImpl)

        binder.bind_to_provider(RoomService, DefaultRoomService)
        binder.bind_to_provider(ProductService, ProductServiceImpl)

        binder.bind_to_provider(SupplierSalesHistoryService, SupplierSalesHistoryServiceImpl)

    inject.configure(config)


def configure_validation_handler(app: FastAPI) -> None:
    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(_: Any, exc: RequestValidationError) -> JSONResponse:
        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            content=jsonable_encoder({"errors": exc.errors()}),
        )


def is_in_stage(stages: List[str]) -> bool:
    return os.getenv("ENV") in stages
