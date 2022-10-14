from src.domain.room.room import RoomOut
from src.infrastructure.adapters.output.repositories.entities import RoomEntity


class RoomMapper:

    @staticmethod
    def entity_to_domain(room: RoomEntity) -> RoomOut:
        if not room:
            return room
        return RoomOut(
            id=room.id,
            name=room.name,
            capacity=room.capacity
        )
