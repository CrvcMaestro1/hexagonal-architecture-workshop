import re
from datetime import datetime, date
from typing import Any

from dataclasses_json import dataclass_json, LetterCase
from pydantic import Field, validator

from src.domain.room.room import RoomOut
from src.domain.utils.date_utils import subtract_days_from_dates, str_to_date
from src.domain.utils.domain_model import DomainModel

DAYS_IN_ADVANCE = 5


class EventBase(DomainModel):
    name: str = Field(max_length=100)
    day: date

    class Config:
        orm_mode = True


@dataclass_json(letter_case=LetterCase.SNAKE)
class EventIn(EventBase):
    room_id: int

    @validator("day", pre=True, always=True, check_fields=False)
    def day_must_be_days_in_advance(cls, v: Any) -> Any:
        today = datetime.now().date()
        day = str_to_date(v)
        subtract_days = subtract_days_from_dates(day, today)
        if subtract_days < DAYS_IN_ADVANCE:
            raise ValueError(f"Day must be {DAYS_IN_ADVANCE} days in advance")
        return v


@dataclass_json(letter_case=LetterCase.SNAKE)
class EventOut(EventBase):
    room: RoomOut
    id: int


@dataclass_json(letter_case=LetterCase.SNAKE)
class EventWithOutRoom(EventBase):
    id: int
