from datetime import date
from typing import List

from src.domain.event.event import EventOut
from src.domain.room.room import RoomOut
from src.domain.utils.date_utils import str_to_date
from src.domain.utils.remote_mapper_validator import RemoteMapperValidator


class PublicEventRemoteMapper(RemoteMapperValidator):
    required_keys = [
        ("id", str),
        ("name", str),
        ("day", date),
        ("room_id", int),
        ("room_name", str),
        ("room_capacity", int),
    ]

    def remote_to_domain(self, data: List) -> List[EventOut]:
        events: list[EventOut] = []
        for datum in data:
            self.is_valid(datum)
            room = RoomOut(id=datum.get("room_id"), name=datum.get("room_name"), capacity=datum.get("room_capacity"))
            event = EventOut(
                id=int(datum.get("id")), name=datum.get("name"),
                day=str_to_date(datum.get("day")),
                room=room
            )
            events.append(event)
        return events
