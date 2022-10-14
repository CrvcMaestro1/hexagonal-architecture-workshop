from typing import List

import inject
from fastapi import APIRouter
from starlette import status
from src.domain.room.input.room_service import RoomService
from src.domain.room.room import RoomIn, RoomOut


@inject.autoparams()
def room_router(
        room_service: RoomService
) -> APIRouter:
    router = APIRouter(tags=["room"])

    @router.get('/rooms', response_model=List[RoomOut], status_code=status.HTTP_200_OK)
    async def room_list() -> List[RoomOut]:
        return room_service.list()

    @router.get('/rooms/{room_id}', response_model=RoomOut, status_code=status.HTTP_200_OK)
    async def get_room(room_id: int) -> RoomOut:
        room = room_service.get(room_id)
        return room

    @router.post('/rooms', response_model=RoomOut, status_code=status.HTTP_201_CREATED)
    async def room_create(room: RoomIn) -> RoomOut:
        room = room_service.create(room)
        return room

    @router.put('/rooms/{room_id}', response_model=RoomOut, status_code=status.HTTP_200_OK)
    async def room_update(room_id: int, room: RoomIn) -> RoomOut:
        room = room_service.update(room_id, room)
        return room

    @router.delete('/rooms/{room_id}', status_code=status.HTTP_204_NO_CONTENT)
    async def room_delete(room_id: int) -> None:
        room_service.delete(room_id)

    return router
