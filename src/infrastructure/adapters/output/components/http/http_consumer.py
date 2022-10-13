import json

from dataclasses import dataclass, field
from enum import Enum
from typing import Optional, Dict

import requests
from requests import HTTPError


@dataclass
class HttpConsumerResponse:
    data: dict = field(default_factory=dict)
    status_code: int = field(default_factory=int)
    is_success: bool = field(default_factory=bool)
    message: str = field(default_factory=str)
    detail: str = field(default_factory=str)


class HttpMethod(Enum):
    GET = "GET"
    POST = "POST"
    PUT = "PUT"
    DELETE = "DELETE"


def is_jsonable(value: Optional[str] = "") -> bool:
    try:
        json.dumps(value)
        json.loads(value)  # type: ignore
        return True
    except (TypeError, OverflowError, Exception):
        return False


class HttpConsumer:

    @staticmethod
    def consume(method: HttpMethod, url: str, headers: Optional[dict] = None,
                json_data: Optional[dict] = None, form_data: Optional[dict] = None,
                require_content_type: Optional[bool] = True) -> HttpConsumerResponse:
        required_headers = {'charset': 'utf-8', 'User-Agent': 'self-service-ms'}
        if require_content_type:
            required_headers.update({'Content-Type': 'application/json'})
        required_headers.update(headers if headers else {})
        response = None
        try:
            response = requests.request(method=method.value, url=url, headers=required_headers, json=json_data,
                                        data=form_data)

            response.raise_for_status()

            return HttpConsumerResponse(
                data=response.json(),
                status_code=response.status_code,
                is_success=True,
                message=response.reason
            )
        except HTTPError as ex:
            http_consumer_response = HttpConsumerResponse()
            http_consumer_response.status_code = 500 if response is None else response.status_code
            http_consumer_response.is_success = False
            http_consumer_response.message = "{}".format(ex)
            error_data: Dict = dict()
            if is_jsonable(response.text):  # type: ignore
                error_data = {} if response is None else response.json()
                error_data["additional"] = response.text.replace('"', '')  # type: ignore
            else:
                error_data["additional"] = "{}".format(ex)
            http_consumer_response.data = error_data
            return http_consumer_response
