from typing import List, Optional, Any

from sqlalchemy import (
    literal_column, insert, update, delete
)
from sqlalchemy.orm import Session

from src.domain.category.category import (
    Category, CategoryCreateIn, CategoryCreateOut, CategoryUpdateIn, CategoryUpdateOut
)
from src.domain.category.output.category_repository import CategoryRepository
from src.infrastructure.adapters.output.repositories.database_engine_config import database_engine, DatabaseEnum
from src.infrastructure.adapters.output.repositories.mapper.category_mapper import (
    CategoryMapper, CategoryCreateOutMapper, CategoryUpdateOutMapper
)
from src.infrastructure.adapters.output.repositories.entities import CategoryEntity


class CategoryRepositoryImpl(CategoryRepository):

    @database_engine(database_type=DatabaseEnum.replica)
    def list(self, **kwargs: Optional[Any]) -> List[Category]:
        with Session(bind=kwargs.get('engine')) as session:
            categories = session.query(CategoryEntity)
            return [CategoryMapper.entity_to_domain(category) for category in categories]

    @database_engine(database_type=DatabaseEnum.replica)
    def get(self, category_id: int, **kwargs: Optional[Any]) -> Category:
        with Session(bind=kwargs.get('engine')) as session:
            category = session.query(CategoryEntity).filter(CategoryEntity.id == category_id).first()
            return CategoryMapper.entity_to_domain(category)

    @database_engine(database_type=DatabaseEnum.master)
    def create(self, category: CategoryCreateIn, **kwargs: Optional[Any]) -> CategoryCreateOut:
        with Session(bind=kwargs.get('engine')) as session:
            query = (
                insert(CategoryEntity)
                .values(**category.dict())
                .returning(literal_column('*'))
            )
            cursor = session.execute(query)
            session.commit()
            result = cursor.fetchone()
            return CategoryCreateOutMapper.entity_to_domain(result)

    @database_engine(database_type=DatabaseEnum.master)
    def update(self, category_id: int, category: CategoryUpdateIn, **kwargs: Optional[Any]) -> CategoryUpdateOut:
        with Session(bind=kwargs.get('engine')) as session:
            query = (
                update(CategoryEntity)
                .values(**category.dict())
                .where(CategoryEntity.id == category_id)
                .returning(literal_column('*'))
            )
            cursor = session.execute(query)
            session.commit()
            result = cursor.fetchone()
            return CategoryUpdateOutMapper.entity_to_domain(result)

    @database_engine(database_type=DatabaseEnum.master)
    def delete(self, category_id: int, **kwargs: Optional[Any]) -> None:
        with Session(bind=kwargs.get('engine')) as session:
            query = (
                delete(CategoryEntity).where(CategoryEntity.id == category_id)
            )
            session.execute(query)
            session.commit()
