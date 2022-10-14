from typing import List
from unittest.mock import Mock

import inject
import pytest

from src.domain.room.room import (
    RoomIn, RoomOut
)
from src.domain.room.default_room_service import DefaultRoomService
from src.domain.room.output.room_repository import RoomRepository


@pytest.fixture
def room_repository() -> Mock:
    return Mock()


@pytest.fixture
def injector(room_repository: Mock) -> None:
    def config(binder: inject.Binder) -> None:
        binder.bind(RoomRepository, room_repository)

    inject.clear_and_configure(config)


@pytest.fixture
def room_in() -> RoomIn:
    return RoomIn(name="Room A", capacity=5)


@pytest.fixture
def room_out() -> RoomOut:
    return RoomOut(id=1, name="Room A", capacity=5)


@pytest.fixture
def rooms() -> List[RoomOut]:
    return [
        RoomOut(id=1, name="Room A", capacity=5),
        RoomOut(id=2, name="Room B", capacity=10),
    ]


class TestDefaultRoomService:
    def test_should_return_list_rooms(
            self, injector: None, room_repository: Mock, rooms: List[RoomOut]) -> None:
        room_repository.list.return_value = rooms
        rooms_result = DefaultRoomService().list()
        assert rooms_result == rooms
        first_room, _ = rooms_result
        assert isinstance(first_room, RoomOut)
        room_repository.list.assert_called_once()

    def test_should_return_room_by_id(
            self, injector: None, room_repository: Mock, room_in: RoomIn) -> None:
        room_repository.get.return_value = room_in
        room_result = DefaultRoomService().get(1)
        assert room_result == room_in
        assert isinstance(room_result, RoomIn)
        room_repository.get.assert_called_once_with(1)

    def test_should_create_room(
            self, injector: None, room_repository: Mock, room_in: RoomIn, room_out: RoomOut
    ) -> None:
        room_repository.create.return_value = room_out
        room_created_result = DefaultRoomService().create(room_in)
        assert room_created_result == room_out
        assert isinstance(room_created_result, RoomOut)
        room_repository.create.assert_called_once_with(room_in)

    def test_should_update_room(
            self, injector: None, room_repository: Mock, room_in: RoomIn, room_out: RoomOut
    ) -> None:
        room_repository.update.return_value = room_out
        room_updated_result = DefaultRoomService().update(1, room_in)
        assert room_updated_result == room_out
        assert isinstance(room_updated_result, RoomOut)
        room_repository.update.assert_called_once_with(1, room_in)

    def test_should_delete_room(
            self, injector: None, room_repository: Mock
    ) -> None:
        DefaultRoomService().delete(1)
        room_repository.delete.assert_called_once_with(1)
