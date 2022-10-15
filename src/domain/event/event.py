import re
from datetime import datetime, date
from typing import Any

from dataclasses_json import dataclass_json, LetterCase
from pydantic import Field, validator

from src.domain.room.room import RoomOut
from src.domain.utils.date_utils import subtract_days_from_dates
from src.domain.utils.domain_model import DomainModel

DAYS_IN_ADVANCE = 5


class EventBase(DomainModel):
    name: str = Field(max_length=25)
    day: date

    class Config:
        orm_mode = True

    @validator("name", pre=True, always=True, check_fields=False)
    def name_must_only_have_letters_numbers_and_spaces(cls, v: Any) -> Any:
        match = re.match("^[a-zA-Z0-9 ]*$", v)
        if not match:
            raise ValueError("Name must only have letters, number and spaces")
        return v

    @validator("day", pre=True, always=True, check_fields=False)
    def day_must_be_days_in_advance(cls, v: Any) -> Any:
        today = datetime.now().date()
        subtract_days = subtract_days_from_dates(v, today)
        if subtract_days < DAYS_IN_ADVANCE:
            raise ValueError(f"Day must be {DAYS_IN_ADVANCE} days in advance")
        return v


@dataclass_json(letter_case=LetterCase.SNAKE)
class EventIn(EventBase):
    room_id: int


@dataclass_json(letter_case=LetterCase.SNAKE)
class EventOut(EventBase):
    room: RoomOut
    id: int


@dataclass_json(letter_case=LetterCase.SNAKE)
class EventWithOutRoom(EventBase):
    id: int
