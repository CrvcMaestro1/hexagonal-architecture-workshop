from abc import abstractmethod
from typing import Optional, TypeVar, List

from dataclasses_json import dataclass_json, LetterCase
from pydantic import BaseModel

from src.domain.utils.remote_mapper_validator import RemoteMapperValidator

T = TypeVar("T", bound=BaseModel)


@dataclass_json(letter_case=LetterCase.SNAKE)
class Paginator(BaseModel):
    count: Optional[int] = None
    next: Optional[str] = None
    previous: Optional[str] = None

    @abstractmethod
    def get_results(self, results: List, validator: Optional[RemoteMapperValidator] = None) -> List[T]:
        pass

    @abstractmethod
    def get_next(self, optional_next: Optional[str] = None) -> Optional[str]:
        pass

    @abstractmethod
    def get_previous(self, optional_previous: Optional[str] = None) -> Optional[str]:
        pass

    @staticmethod
    def _get_value_from_str(key: str, partial_url: str) -> Optional[str]:
        if key in partial_url:
            for part in partial_url.split('&'):
                if key in part and len(part.split('=')) == 2:
                    return part.split('=')[1]
        return None

    def get_pagination(self, optional_page: Optional[str]) -> Optional[str]:
        if optional_page:
            previous_split = optional_page.split("?")
            previous_page = previous_split[1]
            page = self._get_value_from_str('page=', previous_page)
            page_size = self._get_value_from_str('page_size=', previous_page)
            return self._get_pagination_url(page, page_size)
        return None

    @staticmethod
    def _get_pagination_url(page: Optional[str], page_size: Optional[str]) -> str:
        url = ""
        if page:
            url += f"page={page}&"
        if page_size:
            url += f"page_size={page_size}"
        url = url.strip("&")
        return url
