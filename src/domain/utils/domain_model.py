from typing import List, Any, Dict, Union, Mapping, AbstractSet

from pydantic import BaseModel


class DomainModel(BaseModel):
    def dict_exclude(self, exclude_fields: List[str]) -> Dict[str, Any]:
        to_exclude = {}
        for field in exclude_fields:
            to_exclude[field] = True
        return self.dict(exclude=to_exclude)  # type: ignore

    def dict(
            self,
            *,
            include: Union[AbstractSet[Union[int, str]], Mapping[Union[int, str], Any]] = None,
            exclude: Union[AbstractSet[Union[int, str]], Mapping[Union[int, str], Any]] = None,
            by_alias: bool = False,
            skip_defaults: bool = None,
            exclude_unset: bool = False,
            exclude_defaults: bool = False,
            exclude_none: bool = False,
    ) -> Dict[str, Any]:
        return super().dict(
            include=include, exclude=exclude, by_alias=by_alias, skip_defaults=skip_defaults,
            exclude_unset=exclude_unset, exclude_defaults=exclude_defaults, exclude_none=exclude_none
        )
