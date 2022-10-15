from typing import List, Any, Optional

from sqlalchemy import (
    literal_column, insert, update, delete
)
from sqlalchemy.orm import Session

from src.domain.event.event import EventIn, EventOut
from src.domain.event.output.event_repository import EventRepository
from src.infrastructure.adapters.output.repositories.database_engine_config import database_engine, DatabaseEnum
from src.infrastructure.adapters.output.repositories.entities import EventEntity
from src.infrastructure.adapters.output.repositories.mapper.event_mapper import EventMapper, EventWithOutRoomMapper


class DefaultEventRepository(EventRepository):

    @database_engine(database_type=DatabaseEnum.master)
    def list(self, **kwargs: Any) -> List[EventOut]:
        with Session(bind=kwargs.get('engine')) as session:
            events = session.query(EventEntity)
            return [EventMapper.entity_to_domain(event) for event in events]

    @database_engine(database_type=DatabaseEnum.master)
    def get(self, event_id: int, **kwargs: Optional[Any]) -> EventOut:
        with Session(bind=kwargs.get('engine')) as session:
            event = session.query(EventEntity).filter(EventEntity.id == event_id).first()
            return EventMapper.entity_to_domain(event)

    @database_engine(database_type=DatabaseEnum.master)
    def check_if_exists_event_in_the_same_day_by_room(self, event: EventIn) -> bool:
        pass

    @database_engine(database_type=DatabaseEnum.master)
    def create(self, event: EventIn, **kwargs: Optional[Any]) -> EventOut:
        with Session(bind=kwargs.get('engine')) as session:
            query = (
                insert(EventEntity)
                .values(**event.dict())
                .returning(literal_column('*'))
            )
            cursor = session.execute(query)
            session.commit()
            result = cursor.fetchone()
            return EventWithOutRoomMapper.entity_to_domain(result)

    @database_engine(database_type=DatabaseEnum.master)
    def update(self, event_id: int, event: EventIn,  **kwargs: Optional[Any]) -> EventOut:
        with Session(bind=kwargs.get('engine')) as session:
            query = (
                update(EventEntity)
                .values(**event.dict())
                .where(EventEntity.id == event_id)
                .returning(literal_column('*'))
            )
            cursor = session.execute(query)
            session.commit()
            result = cursor.fetchone()
            return EventWithOutRoomMapper.entity_to_domain(result)

    @database_engine(database_type=DatabaseEnum.master)
    def delete(self, event_id: int, **kwargs: Optional[Any]) -> None:
        with Session(bind=kwargs.get('engine')) as session:
            query = (
                delete(EventEntity).where(EventEntity.id == event_id)
            )
            session.execute(query)
            session.commit()

