from src.domain.event.event import EventOut, EventWithOutRoom
from src.domain.room.room import RoomOut
from src.infrastructure.adapters.output.repositories.entities import EventEntity


class EventMapper:

    @staticmethod
    def entity_to_domain(event: EventEntity) -> EventOut:
        if not event:
            return event
        return EventOut(
            id=event.id,
            name=event.name,
            day=event.day,
            room=RoomOut.from_orm(event.room)
        )


class EventWithOutRoomMapper:
    @staticmethod
    def entity_to_domain(event: EventEntity) -> EventWithOutRoom:
        if not event:
            return event
        return EventWithOutRoom(
            id=event.id,
            name=event.name,
            day=event.day
        )
