from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from src.configuration import (
    configure_inject, configure_validation_handler
)
from src.infrastructure.adapters.input.http.utils.error_handler import ErrorHandler
from src.infrastructure.adapters.input.http.v1 import (
    supplier_sales_history_controller, room_controller
)


def create_application() -> FastAPI:
    application = FastAPI(
        title='Hex Architecture Workshop Microservice',
        description='Hex Architecture Workshop'
    )
    configure_inject()
    configure_validation_handler(application)
    application.add_middleware(ErrorHandler)
    application.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    application.include_router(router=room_controller.room_router(), prefix='/v1')
    application.include_router(router=supplier_sales_history_controller.supplier_sales_history_router(),
                               prefix='/v1')
    return application


app = create_application()
