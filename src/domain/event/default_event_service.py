from typing import List

import inject

from src.domain.event.input.event_service import EventService
from src.domain.event.output.event_repository import EventRepository
from src.domain.event.event import EventIn, EventOut, EventWithOutRoom

from src.domain.event.output.public_event_repository import PublicEventRepository
from src.domain.utils.exceptions import ApplicationError


class DefaultEventService(EventService):

    @inject.autoparams()
    def __init__(self, repository: EventRepository, public_repository: PublicEventRepository):
        self.repository = repository
        self.public_repository = public_repository

    def list(self) -> List[EventOut]:
        return self.repository.list()

    def list_public_events(self) -> List[EventOut]:
        return self.public_repository.list_public_events()

    def get(self, event_id: int) -> EventOut:
        event = self.repository.get(event_id)
        if not event:
            raise ApplicationError(404, 'Event does not found')
        return event

    def check_if_exists_event_in_the_same_day_by_room(self, event: EventIn) -> bool:
        return self.repository.check_if_exists_event_in_the_same_day_by_room(event)

    def create(self, event: EventIn) -> EventWithOutRoom:
        if self.check_if_exists_event_in_the_same_day_by_room(event):
            raise ApplicationError(400, 'It is not allowed to create events in the same room on the same day')
        return self.repository.create(event)

    def update(self, event_id: int, event: EventIn) -> EventWithOutRoom:
        return self.repository.update(event_id, event)

    def delete(self, event_id: int) -> None:
        self.repository.delete(event_id)
