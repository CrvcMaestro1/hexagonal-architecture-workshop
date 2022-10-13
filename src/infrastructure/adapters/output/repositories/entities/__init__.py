import enum
from typing import List

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import DeclarativeMeta

Base: DeclarativeMeta = declarative_base()


class Schemas(enum.Enum):
    public = "public"
    test = "test"
    self_services = "self_services"

    @classmethod
    def list(cls) -> List:
        return [e.value for e in cls]


from src.infrastructure.adapters.output.repositories.entities.category_entity import CategoryEntity  # noqa: E402 F401
from src.infrastructure.adapters.output.repositories.entities.product_entity import ProductEntity  # noqa: E402 F401