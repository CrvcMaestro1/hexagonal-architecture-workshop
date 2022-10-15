from abc import (
    ABCMeta,
    abstractmethod
)
from typing import List

from src.domain.event.event import (
    EventIn, EventOut
)


class EventService(metaclass=ABCMeta):

    @abstractmethod
    def list(self) -> List[EventOut]:
        pass

    @abstractmethod
    def list_public_events(self) -> List[EventOut]:
        pass

    @abstractmethod
    def get(self, event_id: int) -> EventOut:
        pass

    @abstractmethod
    def check_if_exists_event_in_the_same_day_by_room(self, event: EventIn) -> bool:
        pass

    @abstractmethod
    def create(self, event: EventIn) -> EventOut:
        pass

    @abstractmethod
    def update(self, event_id: int, event: EventIn) -> EventOut:
        pass

    @abstractmethod
    def delete(self, event_id: int) -> None:
        pass
