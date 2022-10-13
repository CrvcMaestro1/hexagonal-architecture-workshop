from typing import List, Any, Optional

from sqlalchemy import (
    literal_column, insert, update, delete
)
from sqlalchemy.orm import Session

from src.domain.product.output.product_repository import ProductRepository
from src.domain.product.product import Product, ProductCreateOut, ProductCreateIn, ProductUpdateIn, ProductUpdateOut
from src.infrastructure.adapters.output.repositories.database_engine_config import database_engine, DatabaseEnum
from src.infrastructure.adapters.output.repositories.mapper.product_mapper import (
    ProductMapper, ProductCreateOutMapper, ProductUpdateOutMapper
)
from src.infrastructure.adapters.output.repositories.entities import ProductEntity


class ProductRepositoryImpl(ProductRepository):

    @database_engine(database_type=DatabaseEnum.replica)
    def list(self, **kwargs: Optional[Any]) -> List[Product]:
        with Session(bind=kwargs.get('engine')) as session:
            products = session.query(ProductEntity)
            return [ProductMapper.entity_to_domain(product) for product in products]

    @database_engine(database_type=DatabaseEnum.replica)
    def get(self, product_id: int, **kwargs: Any) -> Product:
        with Session(bind=kwargs.get('engine')) as session:
            product = session.query(ProductEntity).filter(ProductEntity.id == product_id).first()
            return ProductMapper.entity_to_domain(product)

    @database_engine(database_type=DatabaseEnum.master)
    def create(self, product: ProductCreateIn, **kwargs: Optional[Any]) -> ProductCreateOut:
        with Session(bind=kwargs.get('engine')) as session:
            query = (
                insert(ProductEntity)
                .values(**product.dict())
                .returning(literal_column('*'))
            )
            cursor = session.execute(query)
            session.commit()
            result = cursor.fetchone()
            return ProductCreateOutMapper.entity_to_domain(result)

    @database_engine(database_type=DatabaseEnum.master)
    def update(self, product_id: int, product: ProductUpdateIn, **kwargs: Optional[Any]) -> ProductUpdateOut:
        with Session(bind=kwargs.get('engine')) as session:
            query = (
                update(ProductEntity)
                .values(**product.dict())
                .where(ProductEntity.id == product_id)
                .returning(literal_column('*'))
            )
            cursor = session.execute(query)
            session.commit()
            result = cursor.fetchone()
            return ProductUpdateOutMapper.entity_to_domain(result)

    @database_engine(database_type=DatabaseEnum.master)
    def delete(self, product_id: int, **kwargs: Optional[Any]) -> None:
        with Session(bind=kwargs.get('engine')) as session:
            query = (
                delete(ProductEntity).where(ProductEntity.id == product_id)
            )
            session.execute(query)
            session.commit()
