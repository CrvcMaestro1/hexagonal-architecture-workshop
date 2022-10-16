from typing import Any

from dataclasses_json import dataclass_json, LetterCase
from pydantic import Field, validator

from src.domain.utils.domain_model import DomainModel


class RoomBase(DomainModel):
    class Config:
        orm_mode = True

    @validator("capacity", pre=True, always=True, check_fields=False)
    def capacity_must_greater_than_zero(cls, v: Any) -> Any:
        if v < 0:
            raise ValueError("Capacity must greater than zero")
        return v


@dataclass_json(letter_case=LetterCase.SNAKE)
class RoomIn(RoomBase):
    name: str = Field(max_length=25)
    capacity: int = Field(gt=0)


@dataclass_json(letter_case=LetterCase.SNAKE)
class RoomOut(RoomIn):
    id: int
