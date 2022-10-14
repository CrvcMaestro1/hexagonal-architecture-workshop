from abc import (
    ABCMeta,
    abstractmethod
)
from typing import List

from src.domain.room.room import RoomIn, RoomOut


class RoomRepository(metaclass=ABCMeta):

    @abstractmethod
    def list(self) -> List[RoomOut]:
        pass

    @abstractmethod
    def get(self, room_id: int) -> RoomOut:
        pass

    @abstractmethod
    def create(self, room: RoomIn) -> RoomOut:
        pass

    @abstractmethod
    def update(self, room_id: int, room: RoomIn) -> RoomOut:
        pass

    @abstractmethod
    def delete(self, room_id: int) -> None:
        pass
