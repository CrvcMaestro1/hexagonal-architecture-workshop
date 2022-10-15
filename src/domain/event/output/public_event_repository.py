from abc import (
    ABCMeta,
    abstractmethod
)
from typing import List

from src.domain.event.event import EventOut


class PublicEventRepository(metaclass=ABCMeta):

    @abstractmethod
    def list_public_events(self) -> List[EventOut]:
        pass
