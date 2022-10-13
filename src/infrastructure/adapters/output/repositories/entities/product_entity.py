from src.infrastructure.adapters.output.repositories.entities import Base, Schemas
from sqlalchemy import (
    Column, Integer, Text, Numeric, Boolean, ForeignKey
)
from sqlalchemy.orm import relationship

from src.infrastructure.adapters.output.repositories.entities.category_entity import CategoryEntity


class ProductEntity(Base):
    __tablename__ = 'products'
    __table_args__ = {'schema': Schemas.test.value}
    id = Column(Integer, primary_key=True)
    name = Column(Text, nullable=False)
    stock = Column(Numeric, nullable=False)
    price = Column(Numeric, nullable=False)
    pvp = Column(Numeric, nullable=False)
    has_discount = Column(Boolean, nullable=False)
    category_id = Column(Integer, ForeignKey(CategoryEntity.id), nullable=False)  # type: ignore
    category = relationship(CategoryEntity, back_populates="products", lazy=True)
