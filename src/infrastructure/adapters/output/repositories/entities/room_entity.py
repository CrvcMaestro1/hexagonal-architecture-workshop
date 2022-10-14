from src.infrastructure.adapters.output.repositories.entities import Base, Schemas
from sqlalchemy import (
    Column, Integer, Text
)
from sqlalchemy.orm import relationship


class RoomEntity(Base):
    __tablename__ = 'rooms'
    __table_args__ = {'schema': Schemas.test.value}
    id = Column(Integer, primary_key=True)
    name = Column(Text, nullable=False,)
    capacity = Column(Integer, nullable=False)
    events = relationship("EventEntity", back_populates="room", lazy=True)
