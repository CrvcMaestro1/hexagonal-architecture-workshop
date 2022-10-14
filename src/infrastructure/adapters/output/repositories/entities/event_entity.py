from src.infrastructure.adapters.output.repositories.entities import Base, Schemas
from sqlalchemy import (
    Column, Integer, Text, ForeignKey
)
from sqlalchemy.orm import relationship

from src.infrastructure.adapters.output.repositories.entities.room_entity import RoomEntity


class EventEntity(Base):
    __tablename__ = 'events'
    __table_args__ = {'schema': Schemas.test.value}
    id = Column(Integer, primary_key=True)
    name = Column(Text, nullable=False)
    room_id = Column(Integer, ForeignKey(RoomEntity.id), nullable=False)  # type: ignore
    room = relationship(RoomEntity, back_populates="events", lazy=True)
