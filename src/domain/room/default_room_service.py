from typing import List

import inject

from src.domain.room.input.room_service import RoomService
from src.domain.room.output.room_repository import RoomRepository
from src.domain.room.room import RoomIn, RoomOut
from src.domain.utils.exceptions import ApplicationError


class DefaultRoomService(RoomService):

    @inject.autoparams()
    def __init__(self, repository: RoomRepository):
        self.repository = repository

    def list(self) -> List[RoomOut]:
        return self.repository.list()

    def get(self, room_id: int) -> RoomOut:
        room = self.repository.get(room_id)
        if not room:
            raise ApplicationError(404, 'Room does not found')
        return room

    def create(self, room: RoomIn) -> RoomOut:
        return self.repository.create(room)

    def update(self, room_id: int, room: RoomIn) -> RoomOut:
        return self.repository.update(room_id, room)

    def delete(self, room_id: int) -> None:
        self.repository.delete(room_id)
