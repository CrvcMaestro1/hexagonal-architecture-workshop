from typing import Optional, Dict, Any

from fastapi import Request, FastAPI
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import Response, JSONResponse

from src.domain.utils.exceptions import ApplicationError


class ExceptionResponse:
    def __init__(self, message: str, data: Optional[dict] = None):
        self.message = message
        self.data = data

    def serialize(self) -> Dict:
        return self.__dict__


class ErrorHandler(BaseHTTPMiddleware):
    def __init__(self, app: FastAPI) -> None:
        super().__init__(app)

    async def dispatch(self, request: Request, call_next: Any) -> Response | JSONResponse:
        try:
            return await call_next(request)
        except ApplicationError as e:
            response = ExceptionResponse(e.message, data=e.data)
            return JSONResponse(status_code=e.code, content=response.serialize())
        except Exception as ex:
            response = ExceptionResponse(f"{ex}")
            return JSONResponse(status_code=500, content=response.serialize())
