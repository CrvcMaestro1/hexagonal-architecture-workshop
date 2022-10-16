from datetime import date, datetime
from typing import Dict, Any

from src.domain.utils.date_utils import str_to_date
from src.domain.utils.exceptions import ApplicationError


class RemoteMapperValidator:
    required_keys: list = []

    def is_valid(self, data: Dict | list) -> bool:
        if isinstance(data, dict):
            self.validator(data)
        else:
            for datum in data:
                self.is_valid(datum)
        return True

    def validator(self, data: Dict) -> bool:
        if not data:
            raise ApplicationError(404, "No info found in third party service.")
        message = "An error occurred in the data validation of the third party service. "
        for required_key in self.required_keys:
            key_name = required_key[0]
            type_field = required_key[1]
            value = data.get(key_name)
            if value is None:
                raise ApplicationError(400, f"{message}{required_key[0]} field is required")
            try:
                parsed_value = self.parser(type_field, value)
                if not isinstance(parsed_value, type_field):
                    raise ApplicationError(400, f"{message}{required_key[0]} must be a field of type {type_field}")
            except ValueError:
                raise ApplicationError(400, f"{message}{required_key[0]} must be a field of type {type_field}")
        return True

    @staticmethod
    def parser(type_field: Any, value: Any) -> Any:
        if type_field is date:
            return str_to_date(value)
        return type_field(value)
