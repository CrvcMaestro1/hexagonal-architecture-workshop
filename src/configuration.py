import os
from typing import List, Any

import inject
from fastapi import FastAPI
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from starlette import status
from starlette.responses import JSONResponse

from src.domain.event.default_event_service import DefaultEventService
from src.domain.event.input.event_service import EventService
from src.domain.event.output.event_repository import EventRepository
from src.domain.event.output.public_event_repository import PublicEventRepository
from src.domain.room.default_room_service import DefaultRoomService
from src.domain.room.input.room_service import RoomService
from src.domain.room.output.room_repository import RoomRepository

from src.infrastructure.adapters.output.remote.remote_public_event_repository import RemotePublicEventRepository
from src.infrastructure.adapters.output.repositories.default_event_repository import DefaultEventRepository
from src.infrastructure.adapters.output.repositories.default_room_repository import DefaultRoomRepository


def configure_inject() -> None:
    def config(binder: inject.Binder) -> None:
        binder.bind_to_provider(RoomRepository, DefaultRoomRepository)
        binder.bind_to_provider(EventRepository, DefaultEventRepository)
        binder.bind_to_provider(PublicEventRepository, RemotePublicEventRepository)

        binder.bind_to_provider(RoomService, DefaultRoomService)
        binder.bind_to_provider(EventService, DefaultEventService)

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
