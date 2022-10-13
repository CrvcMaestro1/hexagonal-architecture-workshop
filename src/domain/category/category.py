from dataclasses_json import dataclass_json, LetterCase
from pydantic import BaseModel


@dataclass_json(letter_case=LetterCase.SNAKE)
class CategoryBase(BaseModel):
    pass


@dataclass_json(letter_case=LetterCase.SNAKE)
class Category(CategoryBase):
    id: int
    name: str

    class Config:
        orm_mode = True


@dataclass_json(letter_case=LetterCase.SNAKE)
class CategoryCreateIn(CategoryBase):
    name: str


@dataclass_json(letter_case=LetterCase.SNAKE)
class CategoryCreateOut(CategoryCreateIn):
    id: int


@dataclass_json(letter_case=LetterCase.SNAKE)
class CategoryUpdateIn(CategoryBase):
    name: str


@dataclass_json(letter_case=LetterCase.SNAKE)
class CategoryUpdateOut(CategoryUpdateIn):
    id: int
