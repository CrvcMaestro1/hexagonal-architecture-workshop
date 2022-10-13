from src.infrastructure.adapters.output.repositories.entities import Base, Schemas
from sqlalchemy import (
    Column, Integer, Text
)
from sqlalchemy.orm import relationship


class CategoryEntity(Base):
    __tablename__ = 'categories'
    __table_args__ = {'schema': Schemas.test.value}
    id = Column(Integer, primary_key=True)
    name = Column(Text, nullable=False)
    products = relationship("ProductEntity", back_populates="category", lazy=True)
