from typing import List, Optional, Any

from sqlalchemy import (
    literal_column, insert, update, delete
)
from sqlalchemy.orm import Session

from src.domain.room.output.room_repository import RoomRepository
from src.domain.room.room import RoomIn, RoomOut
from src.infrastructure.adapters.output.repositories.database_engine_config import database_engine, DatabaseEnum
from src.infrastructure.adapters.output.repositories.entities import RoomEntity
from src.infrastructure.adapters.output.repositories.mapper.room_mapper import RoomMapper


class DefaultRoomRepository(RoomRepository):

    @database_engine(database_type=DatabaseEnum.master)
    def list(self, **kwargs: Optional[Any]) -> List[RoomOut]:
        with Session(bind=kwargs.get('engine')) as session:
            rooms = session.query(RoomEntity)
            return [RoomMapper.entity_to_domain(room) for room in rooms]

    @database_engine(database_type=DatabaseEnum.master)
    def get(self, room_id: int, **kwargs: Optional[Any]) -> RoomOut:
        with Session(bind=kwargs.get('engine')) as session:
            room = session.query(RoomEntity).filter(RoomEntity.id == room_id).first()
            return RoomMapper.entity_to_domain(room)

    @database_engine(database_type=DatabaseEnum.master)
    def create(self, room: RoomIn, **kwargs: Optional[Any]) -> RoomOut:
        with Session(bind=kwargs.get('engine')) as session:
            query = (
                insert(RoomEntity)
                .values(**room.dict())
                .returning(literal_column('*'))
            )
            cursor = session.execute(query)
            session.commit()
            result = cursor.fetchone()
            return RoomMapper.entity_to_domain(result)

    @database_engine(database_type=DatabaseEnum.master)
    def update(self, room_id: int, room: RoomIn, **kwargs: Optional[Any]) -> RoomOut:
        with Session(bind=kwargs.get('engine')) as session:
            query = (
                update(RoomEntity)
                .values(**room.dict())
                .where(RoomEntity.id == room_id)
                .returning(literal_column('*'))
            )
            cursor = session.execute(query)
            session.commit()
            result = cursor.fetchone()
            return RoomMapper.entity_to_domain(result)

    @database_engine(database_type=DatabaseEnum.master)
    def delete(self, room_id: int, **kwargs: Optional[Any]) -> None:
        with Session(bind=kwargs.get('engine')) as session:
            query = (
                delete(RoomEntity).where(RoomEntity.id == room_id)
            )
            session.execute(query)
            session.commit()
