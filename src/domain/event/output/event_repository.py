from abc import (
    ABCMeta,
    abstractmethod
)
from typing import List

from src.domain.event.event import EventIn, EventOut, EventWithOutRoom


class EventRepository(metaclass=ABCMeta):

    @abstractmethod
    def list(self) -> List[EventOut]:
        pass

    @abstractmethod
    def get(self, event_id: int) -> EventOut:
        pass

    @abstractmethod
    def check_if_exists_event_in_the_same_day_by_room(self, event: EventIn) -> bool:
        pass

    @abstractmethod
    def create(self, event: EventIn) -> EventWithOutRoom:
        pass

    @abstractmethod
    def update(self, event_id: int, event: EventIn) -> EventWithOutRoom:
        pass

    @abstractmethod
    def delete(self, event_id: int) -> None:
        pass
