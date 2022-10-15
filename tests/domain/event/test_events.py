import datetime
from datetime import date
from typing import List
from unittest.mock import Mock

import inject
import pytest

from src.domain.event.event import (
    EventIn, EventOut, DAYS_IN_ADVANCE
)
from src.domain.event.default_event_service import DefaultEventService
from src.domain.event.output.event_repository import EventRepository
from src.domain.event.output.public_event_repository import PublicEventRepository

from src.domain.room.room import RoomOut
from src.domain.utils.exceptions import ApplicationError


@pytest.fixture
def event_repository() -> Mock:
    return Mock()


@pytest.fixture
def public_event_repository() -> Mock:
    return Mock()


@pytest.fixture
def injector(event_repository: Mock, public_event_repository: Mock) -> None:
    def config(binder: inject.Binder) -> None:
        binder.bind(EventRepository, event_repository)
        binder.bind(PublicEventRepository, public_event_repository)

    inject.clear_and_configure(config)


@pytest.fixture
def room() -> RoomOut:
    return RoomOut(id=1, name="Room A", capacity=5)


@pytest.fixture
def event_in(room: RoomOut) -> EventIn:
    return EventIn(name="Event A", room_id=room.id, day=date(2022, 10, 20))


@pytest.fixture
def event_out(room: RoomOut) -> EventOut:
    return EventOut(id=1, name="Event A", room=room, day=date(2022, 10, 20))


@pytest.fixture
def events(room: RoomOut) -> List[EventOut]:
    return [
        EventOut(id=1, name="Event A", room=room, day=date(2022, 10, 20)),
        EventOut(id=2, name="Event B", room=room, day=date(2022, 10, 21))
    ]


class TestDefaultRoomService:
    def test_should_return_list_events(
            self, injector: None, event_repository: Mock, events: List[EventOut]) -> None:
        event_repository.list.return_value = events
        events_result = DefaultEventService().list()
        assert events_result == events
        first_event, _ = events_result
        assert isinstance(first_event, EventOut)
        event_repository.list.assert_called_once()

    def test_should_return_event_by_id(
            self, injector: None, event_repository: Mock, event_in: EventIn) -> None:
        event_repository.get.return_value = event_in
        event_result = DefaultEventService().get(1)
        assert event_result == event_in
        assert isinstance(event_result, EventIn)
        event_repository.get.assert_called_once_with(1)

    def test_should_create_event(
            self, injector: None, event_repository: Mock, event_in: EventIn, event_out: EventOut
    ) -> None:
        event_repository.create.return_value = event_out
        event_repository.check_if_exists_event_in_the_same_day_by_room.return_value = False
        event_created_result = DefaultEventService().create(event_in)
        assert event_created_result == event_out
        assert isinstance(event_created_result, EventOut)
        event_repository.create.assert_called_once_with(event_in)

    def test_should_update_event(
            self, injector: None, event_repository: Mock, event_in: EventIn, event_out: EventOut
    ) -> None:
        event_repository.update.return_value = event_out
        event_updated_result = DefaultEventService().update(1, event_in)
        assert event_updated_result == event_out
        assert isinstance(event_updated_result, EventOut)
        event_repository.update.assert_called_once_with(1, event_in)

    def test_should_delete_event(
            self, injector: None, event_repository: Mock
    ) -> None:
        DefaultEventService().delete(1)
        event_repository.delete.assert_called_once_with(1)

    def test_should_raise_an_error_with_past_due_event(
            self, injector: None, event_repository: Mock, room: RoomOut
    ) -> None:
        today = datetime.datetime.now().date()
        with pytest.raises(ValueError, match=f"Day must be {DAYS_IN_ADVANCE} days in advance"):
            EventOut(id=1, name="Event A", room=room, day=today)

    def test_should_raise_an_error_with_event_repeated_on_same_date(
            self, injector: None, event_repository: Mock, event_in: EventIn, event_out: EventOut
    ) -> None:
        # first event
        event_repository.create.return_value = event_out
        event_repository.check_if_exists_event_in_the_same_day_by_room.return_value = False
        DefaultEventService().create(event_in)
        # second event - repeated
        event_repository.check_if_exists_event_in_the_same_day_by_room.return_value = True
        with pytest.raises(
                ApplicationError, match="It is not allowed to create events in the same room on the same day"
        ):
            DefaultEventService().create(event_in)

    def test_should_return_list_public_events(
            self, injector: None, public_event_repository: Mock, events: List[EventOut]
    ) -> None:
        public_event_repository.list_public_events.return_value = events
        public_events_result = DefaultEventService().list_public_events()
        assert public_events_result == events
        first_event, _ = public_events_result
        assert isinstance(first_event, EventOut)
        public_event_repository.list_public_events.assert_called_once()
