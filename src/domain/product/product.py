from dataclasses_json import dataclass_json, LetterCase
from pydantic import BaseModel

from src.domain.category.category import Category


@dataclass_json(letter_case=LetterCase.SNAKE)
class ProductBase(BaseModel):
    pass


@dataclass_json(letter_case=LetterCase.SNAKE)
class Product(ProductBase):
    id: int
    name: str
    stock: float
    price: float
    pvp: float
    has_discount: bool
    category: Category

    class Config:
        orm_mode = True


@dataclass_json(letter_case=LetterCase.SNAKE)
class ProductCreateIn(ProductBase):
    name: str
    stock: float
    price: float
    pvp: float
    has_discount: bool
    category_id: int


@dataclass_json(letter_case=LetterCase.SNAKE)
class ProductCreateOut(ProductCreateIn):
    id: int


@dataclass_json(letter_case=LetterCase.SNAKE)
class ProductUpdateIn(ProductBase):
    name: str
    stock: float
    price: float
    pvp: float
    has_discount: bool
    category_id: int


@dataclass_json(letter_case=LetterCase.SNAKE)
class ProductUpdateOut(ProductUpdateIn):
    id: int
